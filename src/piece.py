from src.color import *


class Piece:

    def __init__(self, tiles):
        self.tiles = tiles

        self.board_x = None
        self.board_y = None

    def tiles_width(self):
        return len(self.tiles[0])

    def tiles_height(self):
        return len(self.tiles)

    def rotate_tiles_cw(self):
        self.tiles = [[self.tiles[y][x] for y in range(self.tiles_height() - 1, -1, -1)]
                      for x in range(self.tiles_width())]

    def rotate_tiles_ccw(self):
        self.tiles = [[self.tiles[y][x] for y in range(self.tiles_height())]
                      for x in range(self.tiles_width() - 1, -1, -1)]


PIECES = {
    'I': (CYAN, [[0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0]]),

    'O': (YELLOW, [[1, 1],
                   [1, 1]]),

    'T': (PURPLE, [[0, 0, 0],
                   [1, 1, 1],
                   [0, 1, 0]]),

    'S': (GREEN, [[0, 0, 0],
                  [0, 1, 1],
                  [1, 1, 0]]),

    'Z': (RED, [[0, 0, 0],
                [1, 1, 0],
                [0, 1, 1]]),

    'J': (BLUE, [[0, 0, 0],
                 [1, 1, 1],
                 [0, 0, 1]]),

    'L': (ORANGE, [[0, 0, 0],
                   [1, 1, 1],
                   [1, 0, 0]]),
}
