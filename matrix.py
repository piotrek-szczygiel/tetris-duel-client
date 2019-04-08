from typing import List, Optional

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
        self.vanish = config.rows

        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height + self.vanish)]

    def collision(self, piece: Piece) -> bool:
        grid = piece.get_grid()
        x = piece.x + grid.x
        y = piece.y + grid.y

        if x < 0 or x + grid.width > self.width:
            return True

        if y + grid.height <= self.vanish:
            return False

        if y + grid.height > self.height + self.vanish:
            return True

        for my in range(grid.height):
            if y + my < self.vanish:
                continue

            for mx in range(grid.width):
                c = grid.grid[my + grid.y][mx + grid.x]
                if c != 0 and self.grid[y + my][x + mx] != 0:
                    return True

        return False

    def lock(self, piece: Piece) -> bool:
        grid = piece.get_grid()
        x = piece.x + grid.x
        y = piece.y + grid.y

        if y + grid.height <= self.vanish:
            return False

        for my in range(grid.height):
            for mx in range(grid.width):
                c = grid.grid[my + grid.y][mx + grid.x]
                if c != 0:
                    self.grid[y + my][x + mx] = c

        return True

    def get_full_rows(self) -> List[int]:
        rows = []
        for y in range(self.height + self.vanish):
            full = True
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    full = False
                    break

            if full:
                rows.append(y)

        return rows

    def clear_row(self, row: int) -> None:
        for y in range(row, 0, -1):
            for x in range(self.width):
                self.grid[y][x] = self.grid[y - 1][x]

    def get_ghost(self, piece: Piece) -> Optional[Piece]:
        ghost = Piece(piece.shape, piece.rotation, piece.x, piece.y, ghost=True)
        if ghost.fall(self.collision) > 1:
            return ghost
        return None

    def draw(self, x: int, y: int) -> None:
        size = config.size

        self.draw_grid(x, y)

        for my in range(self.height):
            for mx in range(self.width):
                if self.grid[self.vanish + my][mx] == 0:
                    continue

                draw_block(SHAPE_COLORS[self.grid[self.vanish + my][mx]],
                           x + mx * size,
                           y + my * size,
                           size,
                           224)

    def draw_grid(self, x: int, y: int):
        size = config.size
        grid_color = (32, 32, 64, 128)

        for row in range(self.height + 1):
            pygame.draw.line(ctx.surface,
                             grid_color,
                             (x, y + row * size),
                             (x + size * self.width, y + row * size),
                             3)

        for column in range(self.width + 1):
            pygame.draw.line(ctx.surface,
                             grid_color,
                             (x + column * size, y),
                             (x + column * size, y + size * self.height),
                             3)
