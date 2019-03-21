import pygame
from blinker import signal

from colors import *
from config import SIZE


class Board:
    def __init__(self):
        self.cols = 10
        self.rows = 20
        self.board = None
        self.surface = None

        self.board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]

        self.surface = pygame.Surface((
            self.cols * SIZE,
            self.rows * SIZE
        ))

    def place(self, piece, x, y):
        for piece_y in range(piece.tiles_height()):
            for piece_x in range(piece.tiles_width()):
                if piece.tiles[piece_y][piece_x] == 0:
                    continue

                self.board[y + piece_y][x + piece_x] = piece.color

    def render(self):
        self.surface.fill(BACKGROUND_RGB)

        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == 0:
                    continue

                self.render_block(self.board[y][x], x, y, SIZE)

    def render_block(self, color, x, y, size):
        pygame.draw.rect(self.surface,
                         RGB_COLORS[color],
                         pygame.Rect(x * size, y * size, size, size))
