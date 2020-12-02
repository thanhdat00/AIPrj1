import pygame as p
import GameEngine
import time
from tkinter import *
from tkinter import messagebox
import Block

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

    def heuristic(self):
       return

    def quickMove(self, desRow, desCol):
        return

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