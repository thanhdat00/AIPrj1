import pygame as p
import GameEngine

class Graphic:
    WIDTH = HEIGHT = 512
    DIMENSION = 15
    SQ_SIZE = HEIGHT // DIMENSION
    MAX_SPF = 15
    IMAGES = {}

    def __init__(self):
        p.init()
        screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        gs = GameEngine.GameState()
        self.loadImage()
        running = True
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
            self.drawGameState(screen, gs)
            clock.tick(self.MAX_SPF)
            p.display.flip()

    def loadImage(self):
         pieces =['hider' , 'seeker', 'crate']
         for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (self.SQ_SIZE, self.SQ_SIZE))



    def drawBoard(self,screen):
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                color = colors[((r+c)%2)]
                p.draw.rect(screen, color, p.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))


    def drawPieces(self,screen, board):
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = board[r][c]
                if piece != "--":
                    screen.blit(self.IMAGES[piece], p.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))


    def drawGameState(self,screen, gs):
        self.drawBoard(screen)
        self.drawPieces(screen, gs.board)