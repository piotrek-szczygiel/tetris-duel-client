import math
from random import randint
from typing import List, Tuple

import pygame as pg

from block import draw_block
from config import config
from ctx import ctx
from piece import Piece
from shape import GARBAGE_COLOR, SHAPE_COLORS

Grid = List[List[int]]


class Matrix:
    def __init__(self) -> None:
        self.width = 10

        self.height = 20
        self.vanish = 20
        self.grid: Grid

        self.clear()

    def clear(self) -> None:
        self.grid = [
            [0 for _ in range(self.width)]
            for _ in range(self.height + self.vanish)
        ]

    def debug_add(self, bricks: List[Tuple[int, int]]) -> None:
        self.clear()
        for y, x in bricks:
            self.grid[y][x] = randint(1, 7)

    def debug_tower(self) -> None:
        bricks = [
            (39, 0),
            (39, 1),
            (38, 0),
            (37, 0),
            (37, 1),
            (36, 0),
            (36, 1),
            (35, 0),
            (34, 0),
            (34, 1),
            (33, 0),
            (33, 1),
            (32, 0),
            (31, 0),
            (31, 1),
            (30, 0),
            (30, 1),
            (29, 0),
            (28, 0),
            (28, 1),
            (26, 2),
            (25, 2),
        ]

        for y in range(14):
            bricks.append((39 - y, 3))

        for y in range(12):
            for x in range(4, 10):
                bricks.append((39 - y, x))

        self.debug_add(bricks)

    def get_grid(self) -> Grid:
        return self.grid

    def collision(self, piece: Piece) -> bool:
        grid = piece.get_grid()
        x = piece.x + grid.x
        y = piece.y + grid.y

        if x < 0 or x + grid.width > self.width:
            return True

        if y + grid.height > self.height + self.vanish:
            return True

        for my in range(grid.height):
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

    def collapse_row(self, row: int) -> None:
        for y in range(row, 0, -1):
            for x in range(self.width):
                self.grid[y][x] = self.grid[y - 1][x]

    def erase_row(self, row: int) -> None:
        for x in range(self.width):
            self.grid[row][x] = 0

    def add_garbage(self, hole: int) -> None:
        for y in range(self.height + self.vanish - 1):
            for x in range(self.width):
                self.grid[y][x] = self.grid[y + 1][x]

        for x in range(self.width):
            if x != hole:
                self.grid[self.height + self.vanish - 1][x] = GARBAGE_COLOR
            else:
                self.grid[self.height + self.vanish - 1][x] = 0

    def get_ghost(self, piece: Piece) -> Piece:
        ghost = Piece(
            piece.shape, piece.rotation, piece.x, piece.y, ghost=True
        )
        ghost.fall(self.collision)
        return ghost

    def draw(self, x: int, y: int) -> None:
        size = 30

        self.draw_grid(x, y)

        for my in range(-1, self.height):
            for mx in range(self.width):
                if self.grid[self.vanish + my][mx] == 0:
                    continue

                alpha = 0.7
                if my == -1:
                    alpha = 0.3

                draw_block(
                    SHAPE_COLORS[self.grid[self.vanish + my][mx]],
                    x + mx * size,
                    y + my * size,
                    size,
                    alpha,
                )

    def draw_grid(self, x: int, y: int) -> None:

        # make grid wider on smaller resolutions
        display_w = pg.display.get_surface().get_size()[0]
        starting_w = config.window_size[0]
        width = math.ceil(starting_w / display_w)

        size = 30
        grid_color = (32, 32, 32)

        for row in range(self.height + 1):
            pg.draw.line(
                ctx.surface,
                grid_color,
                (x, y + row * size),
                (x + size * self.width, y + row * size),
                width,
            )

        for column in range(self.width + 1):
            pg.draw.line(
                ctx.surface,
                grid_color,
                (x + column * size, y),
                (x + column * size, y + size * self.height),
                width,
            )
