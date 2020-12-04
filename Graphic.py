import pygame as p
import GameEngine
from queue import Queue
import numpy as np

import time
from tkinter import *
from tkinter import messagebox
import Block

checked = np.zeros((15,15))

class Graphic:
    WIDTH = HEIGHT = 512
    DIMENSION = 15
    SQ_SIZE = HEIGHT // DIMENSION
    MAX_SPF = 15
    IMAGES = {}
    colors = [p.Color("white"), p.Color("gray")]
    seekerRowPos = -1
    seekerColPos = -1
    hiderRowPos = -1
    hiderColPos = -1
    direction = [[0,-1], [0,1], [-1,0], [1,0], [1,1],      [-1,1] ,        [-1,-1],  [1,-1]]
                # 0.Left  1.Right 2.Down 3.Up   4.Down-Right 5.Up-Right   6.Up-Left   7.Down-Left
    gs = None
    leftOrRight = 0


    # init component
    def __init__(self, map, seekerRowPos, seekerColPos, hiderRowPos, hiderColPos):
        p.init()
        self.seekerRowPos = seekerRowPos
        self.seekerColPos = seekerColPos
        self.hiderRowPos = hiderRowPos
        self.hiderColPos = hiderColPos
        self.gs = GameEngine.GameState(map)
        self.loadImage()

    def run(self):
        screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        running = True

        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

            self.drawGameState(screen, self.gs)
            clock.tick(self.MAX_SPF)
            p.display.flip()
            # if self.gameOver():
            #     return
            #     # Tk().wm_withdraw()
            #     # messagebox.showinfo('Game Over')
            # else :
            #     if self.leftOrRight == 0 :
            #         self.searchRight()
            #     else :
            #         self.searchLeft()
            # time.sleep(0.2)

    def searchRight(self):
        if self.seekerColPos != 14:
            self.moveRight()
        elif self.seekerColPos == 14:
            self.moveDown()
            self.leftOrRight = 1

    def searchLeft(self):
        if self.seekerColPos != 0:
            self.moveLeft()
        elif self.seekerColPos == 0:
            self.moveDown()
            self.leftOrRight = 0

    #check if sight is blocked from (x1,y1) to (x2,y2)
    def sightBlocked(self, x1, y1, x2, y2):
        queue = Queue(maxsize=60)
        visited = []
        queue.put((x1,y1))

        while not queue.empty():
           cell = queue.get()
           visited.append(cell)

           if cell[0] == x2 and cell[1]== y2:
               return False
           distance = self.distance(cell[0],cell[1],x2,y2)
           if (self.lineIntersectsCell(x1+0.5,y1+0.5,x2+0.5,y2+0.5,cell[0],cell[1])):
                if (self.inMap(cell[0],cell[1]) and self.gs.board[cell[0]][cell[1]] != 1):
                    for i in range(8):
                        delta = self.direction[i]
                        nx = delta[0] + cell[0]
                        ny = delta[1] + cell[1]
                        #not visit and closer
                        if (not visited.__contains__((nx,ny))  and self.distance(nx,ny,x2,y2)<= distance):
                            queue.put((nx,ny))
        #default sight is blocked
        return True

    def heuristic(self):
        h = []
        for i in range (self.MAX_SPF):
            r = []
            for j in range(self.MAX_SPF):
                r.append(0)
            h.append(r)

        for i in range(self.MAX_SPF):
            for j in range(self.MAX_SPF):
                if (self.gs.board[i][j] != 1):
                    x1 = max(0,i-3)
                    y1 = max(0,j-3)
                    x2 = min(self.MAX_SPF,i+4)
                    y2 = min(self.MAX_SPF,j+4)
                    for x in range (x1,x2):
                        for y in range (y1,y2):
                            if (x!=i and y!=j):
                                if (self.gs.board[x][y] != 1):
                                    if (not self.sightBlocked(i,j,x,y)):
                                        h[i][j] = h[i][j] + 1
                    #right
                    for t in range(j+1,y2):
                        if (self.gs.board[i][t] != 1):
                            h[i][j] = h[i][j] +1
                        else:
                            break

                    #left
                    for t in range(j-1,y1-1,-1):
                        if (self.gs.board[i][t] != 1):
                            h[i][j] = h[i][j] + 1
                        else:
                            break

                    #down
                    for t in range(i+1,x2):
                        if (self.gs.board[t][j] != 1):
                            h[i][j] = h[i][j] + 1
                        else:
                            break

                    #up
                    for t in range(i-1,x1-1,-1):
                        if (self.gs.board[t][j] != 1):
                            h[i][j] = h[i][j] +1
                        else:
                            break


        return h

    def quickMove(self, desRow, desCol):
        return

    def distance(self, r1,c1, r2,c2):
        return abs(r1 - r2) + abs(c1 - c2)

    def observed(self):
        checked[self.seekerRowPos][self.seekerColPos] = 1
        for i in range(self.seekerRowPos - 3, self.seekerRowPos + 4):
            for j in range(self.seekerColPos - 3, self.seekerColPos + 4):
                if self.inMap(i,j):
                    if self.gs.board[i][j] != 1:
                        if self.gs.board[i][j] == 2:
                            return i,j
                        else:
                            if checked[i][j] != 1:
                                if self.notBlock(i,j):
                                    checked[i][j]=1
        return None

    def printChecked(self):
        # for i in range(15):
        #     for j in range(15):
        #         print(checked[i][j])
        for i in range(15):
            for j in range(15):
                print("%3d " % checked[i][j], end='')
            print()

    def printBoard(self):
        # for i in range(15):
        #     for j in range(15):
        #         print(checked[i][j])
        for i in range(15):
            for j in range(15):
                print("%3d " % self.gs.board[i][j], end='')
            print()

    def notBlock(self, x, y):
        # hang ngang
        if x == self.seekerRowPos:
            dis = abs(self.seekerColPos - y) -1
            #ben phai
            if y > self.seekerColPos:
                for i in range (dis):
                    if self.gs.board[x][self.seekerColPos + i +1] == 1:
                        return False
            #ben trai
            if y < self.seekerColPos:
                for i in range (dis):
                    if self.gs.board[x][self.seekerColPos - (i+1)] == 1:
                        return False
        #hang doc
        if y == self.seekerColPos:
            dis = abs(self.seekerRowPos - x) - 1
            #ben tren
            if x < self.seekerRowPos:
                for i in range(dis):
                    if self.gs.board[self.seekerRowPos - (i+1)][y] == 1:
                        return False
            #ben duoi
            if x > self.seekerRowPos:
                for i in range(dis):
                    if self.gs.board[self.seekerRowPos + i+1][y] == 1:
                        return False
        #duong cheo
        if abs(self.seekerRowPos - x) == abs(self.seekerColPos - y):
            dis = abs(self.seekerRowPos - x) -1
            #goc phan tu thu 1
            if self.seekerRowPos > x and self.seekerColPos < y:
                for i in range(dis):
                    if self.gs.board[self.seekerRowPos - (i+1)][self.seekerColPos + i+1] == 1:
                        return False
            #goc phan tu thu 2
            if self.seekerRowPos > x and self.seekerColPos > y:
                for i in range(dis):
                    if self.gs.board[self.seekerRowPos - (i+1)][self.seekerColPos - (i+1)] == 1:
                        return False
            #goc phan tu thu 3
            if self.seekerRowPos < x and self.seekerColPos > y:
                for i in range(dis):
                    if self.gs.board[self.seekerRowPos + (i+1)][self.seekerColPos - (i+1)] == 1:
                        return False
            #goc phan tu thu 4
            if self.seekerRowPos < x and self.seekerColPos < y:
                for i in range(dis):
                    if self.gs.board[self.seekerRowPos + (i+1)][self.seekerColPos + i+1] == 1:
                        return False
        #truong hop dac biet
        #7
        if abs(self.seekerRowPos - x) == 1 and abs(self.seekerColPos - y) == 2:
            colDis = (self.seekerColPos + y) // 2
            if self.gs.board[self.seekerRowPos][colDis] == 1 and self.gs.board[x][colDis] == 1:
                return False
        #5
        if abs(self.seekerRowPos - x) == 2 and abs(self.seekerColPos - y) == 1:
            if self.seekerRowPos > x:
                if self.gs.board[self.seekerRowPos-1][self.seekerColPos] and self.gs.board[x-1][y] == 1:
                    return False
            if self.seekerRowPos < x:
                if self.gs.board[self.seekerRowPos+1][self.seekerColPos] and self.gs.board[x-1][y] == 1:
                    return False
        #10
        if abs(self.seekerRowPos - x) == 3 and abs(self.seekerColPos - y) == 1:
            if self.seekerRowPos > x:
                if self.gs.board[self.seekerRowPos-1][self.seekerColPos] == 1 or self.gs.board[self.seekerRowPos-2][y] == 1:
                    return False
            if self.seekerRowPos < x:
                if self.gs.board[self.seekerRowPos+1][self.seekerColPos] == 1 or self.gs.board[self.seekerRowPos+2][y] == 1:
                    return False
        #11
        if abs(self.seekerRowPos - x) == 3 and abs(self.seekerColPos - y) == 2:
            rowDis = abs(self.seekerRowPos + x) // 2
            colDis = abs(self.seekerColPos + y) // 2
            if self.gs.board[rowDis][colDis] == 1 or self.gs.board[rowDis+1][colDis] == 1:
                return False
        #14
        if abs(self.seekerRowPos - x) == 1 and abs(self.seekerColPos - y) == 3:
            if self.seekerColPos < y:
                if self.gs.board[x][y-1] == 1 or self.gs.board[x-1][y-2] == 1:
                    return False
            if self.seekerColPos > y:
                if self.gs.board[x][y+1] == 1 or self.gs.board[x-1][y+2] == 1:
                    return False
        #13
        if abs(self.seekerRowPos - x) == 2 and abs(self.seekerColPos - y) == 3:
            if self.seekerColPos < y:
                if self.gs.board[x-1][y-1] == 1 or self.gs.board[x-1][y-2] == 1:
                    return False
            if self.seekerColPos > y:
                if self.gs.board[x-1][y+1] == 1 or self.gs.board[x-1][y+2] == 1:
                    return False

        return True

    def search(self):
        return

    def loadImage(self):
         pieces =['hider' , 'seeker', 'crate']
         for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (self.SQ_SIZE, self.SQ_SIZE))

    def drawBoard(self, screen):

        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                color = self.colors[((r+c)%2)]
                p.draw.rect(screen, color, p.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawPieces(self,screen, board):
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = self.decodePiece(board[r][c])
                if piece != "--":
                    screen.blit(self.IMAGES[piece], p.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawGameState(self,screen, gs):
        self.drawBoard(screen)
        self.drawPieces(screen, gs.board)

    def decodePiece(self,c):
        if (c == 0): return '--'
        if (c == 1): return 'crate'
        if (c == 2): return 'hider'
        if (c == 3): return 'seeker'

    def moveUp(self):
        if self.seekerRowPos == 0 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos-1][self.seekerColPos] = 3
        self.seekerRowPos = self.seekerRowPos - 1

    def moveDown(self):
        if self.seekerRowPos == 14 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos+1][self.seekerColPos] = 3
        self.seekerRowPos = self.seekerRowPos + 1

    def moveRight(self):
        if self.seekerColPos == 14 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos][self.seekerColPos + 1] = 3
        self.seekerColPos = self.seekerColPos + 1

    def moveLeft(self):
        if self.seekerColPos == 0 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos][self.seekerColPos - 1] = 3
        self.seekerColPos = self.seekerColPos -1

    def moveUpRight(self):
        if self.seekerRowPos == 0 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos-1][self.seekerColPos+1] = 3
        self.seekerRowPos = self.seekerRowPos - 1
        self.seekerColPos = self.seekerColPos + 1

    def moveUpLeft(self):
        if self.seekerRowPos == 0 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos-1][self.seekerColPos-1] = 3
        self.seekerRowPos = self.seekerRowPos - 1
        self.seekerColPos = self.seekerColPos - 1

    def moveDownRight(self):
        if self.seekerColPos == 0 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos+1][self.seekerColPos+1] = 3
        self.seekerRowPos = self.seekerRowPos + 1
        self.seekerColPos = self.seekerColPos + 1

    def moveDownLeft(self):
        if self.seekerColPos == 0 :
            return
        self.gs.board[self.seekerRowPos][self.seekerColPos] = 0
        self.gs.board[self.seekerRowPos+1][self.seekerColPos-1] = 3
        self.seekerRowPos = self.seekerRowPos + 1
        self.seekerColPos = self.seekerColPos - 1

    def gameOver(self):
        if self.seekerColPos == self.hiderColPos and self.seekerRowPos == self.hiderRowPos:
            return True
        return False

    def distance(self, x1, y1, x2, y2):
        return pow(x2-x1,2) + pow(y2-y1,2)

    def lineIntersectsCell(self, x1, y1, x2, y2, rx, ry):
        rw = 1
        rh = 1
        left = self.lineIntersectLine(x1,y1,x2,y2,rx,ry,rx,ry+rh)
        right = self.lineIntersectLine(x1,y1,x2,y2,rx+rw,ry,rx+rw,ry+rh)
        top = self.lineIntersectLine(x1,y1,x2,y2,rx,ry,rx+rw,ry)
        bottom = self.lineIntersectLine(x1,y1,x2,y2,rx,ry+rh,rx+rw,ry+rh)

        return (left or right or top or bottom)

    def inMap(self, x, y):
        if (x < 0 or y < 0 or x >= 15 or y >= 15):
            return False
        return  True

    def lineIntersectLine(self, x1, y1, x2, y2, x3, y3, x4, y4):
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        if (uA >= 0 and  uA <= 1 and  uB >= 0  and  uB <= 1):
            return True
        return False
