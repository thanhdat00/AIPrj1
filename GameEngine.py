import Block

class GameState():
    def __init__(self, map):
        self.board = map
        self.whiteToMove = True
        self.moveLog = []