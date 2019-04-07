import pygame

import config
import ctx
from block import draw_block
from shape import SHAPE_COLORS


class Matrix:
    def __init__(self) -> None:
        self.width = config.cols
        self.height = config.rows
        self.vanish = 4

        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height + self.vanish)]

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
                if self.grid[my + self.vanish][mx] == 0:
                    continue

                draw_block(SHAPE_COLORS[self.grid[my + self.vanish][mx]],
                           x + mx * size,
                           y + my * size,
                           size,
                           False)
