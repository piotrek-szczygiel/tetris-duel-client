from random import randint

import config
from block import draw_block
from shape import SHAPE_COLORS


class Matrix:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.vanish = 20

        self.grid = [[randint(1, 7) for _ in range(self.width)]
                     for _ in range(self.height + self.vanish)]

    def draw(self, x: int, y: int) -> None:
        size = config.size

        for my in range(self.height):
            for mx in range(self.width):
                if self.grid[my + self.vanish][mx] == 0:
                    continue

                draw_block(SHAPE_COLORS[self.grid[my + self.vanish][mx]],
                           x + mx * size,
                           y + my * size,
                           size,
                           False
                           )
