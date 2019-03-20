import pygame

from src.colors import *
from src.config import SIZE


class Board:
    def __init__(self):
        self.cols = 10
        self.rows = 20
        self.board = None
        self.surface = None

    def initialize(self):
        self.board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]

        self.surface = pygame.Surface((
            self.cols * SIZE,
            self.rows * SIZE
        ))

    def render(self):
        self.surface.fill(BACKGROUND_RGB)

        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == 0:
                    continue

                self.render_block(self.board[y][x], x, y)

    def render_block(self, color, x, y):
        pygame.draw.rect(self.surface,
                         RGB_COLORS[color],
                         pygame.Rect(x * SIZE, y * SIZE, SIZE, SIZE))
