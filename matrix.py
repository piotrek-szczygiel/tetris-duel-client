import pygame

import config
import ctx
from block import draw_block
from piece import Piece
from shape import SHAPE_COLORS


class Matrix:
    def __init__(self) -> None:
        self.width = config.cols
        self.height = config.rows

        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height)]

    def collision(self, piece: Piece) -> bool:
        grid = piece.get_grid()
        x = piece.x + grid.x
        y = piece.y + grid.y

        if y + grid.height <= 0:
            return False

        if (x < 0
                or x + grid.width > self.width
                or y + grid.height > self.height):
            return True

        for my in range(grid.height):
            if y + my < 0:
                continue

            for mx in range(grid.width):
                c = grid.grid[my + grid.y][mx + grid.x]
                if c != 0 and self.grid[y + my][x + mx] != 0:
                    return True

        return False

    def lock(self, piece: Piece) -> None:
        grid = piece.get_grid()
        x = piece.x + grid.x
        y = piece.y + grid.y
        for my in range(grid.height):
            for mx in range(grid.width):
                c = grid.grid[my + grid.y][mx + grid.x]
                if c != 0:
                    self.grid[y + my][x + mx] = c

    def draw(self, x: int, y: int) -> None:
        size = config.size
        grid_color = (48, 48, 96)

        for row in range(self.height + 1):
            pygame.draw.line(ctx.display,
                             grid_color,
                             (x, y + row * size - 1),
                             (x + size * self.width, y + row * size - 1),
                             2)

        for column in range(self.width + 1):
            pygame.draw.line(ctx.display,
                             grid_color,
                             (x + column * size - 1, y),
                             (x + column * size - 1, y + size * self.height),
                             2)

        for my in range(self.height):
            for mx in range(self.width):
                if self.grid[my][mx] == 0:
                    continue

                draw_block(SHAPE_COLORS[self.grid[my][mx]],
                           x + mx * size,
                           y + my * size,
                           size,
                           False)
