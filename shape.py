from dataclasses import dataclass
from typing import List, Tuple

from block import draw_block

WallKicks = Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]


@dataclass
class ShapeGrid:
    x: int
    y: int
    width: int
    height: int
    grid: List[List[int]]


@dataclass
class Shape:
    grid: List[ShapeGrid]
    wall_kicks: List[WallKicks]

    def draw(self, rotation: int, x: int, y: int, size: int) -> None:
        grid = self.grid[rotation]
        height = len(grid.grid)
        width = len(grid.grid[0])

        for my in range(height):
            for mx in range(width):
                c = grid.grid[my][mx]
                if c == 0:
                    continue

                draw_block(SHAPE_COLORS[c],
                           x + mx * size,
                           y + my * size,
                           size,
                           True)


# https://tetris.fandom.com/wiki/SRS

WALL_KICKS_JLSTZ = [
    ([(-1, 0), (-1, -1), (0, 2), (-1, 2)],
     [(1, 0), (1, -1), (0, 2), (1, 2)]),

    ([(1, 0), (1, 1), (0, -2), (1, -2)],
     [(1, 0), (1, 1), (0, -2), (1, -2)]),

    ([(1, 0), (1, -1), (0, 2), (1, 2)],
     [(-1, 0), (-1, -1), (0, 2), (-1, 2)]),

    ([(-1, 0), (-1, 1), (0, -2), (-1, -2)],
     [(-1, 0), (-1, 1), (0, -2), (-1, -2)])]

WALL_KICKS_I = [
    ([(-2, 0), (1, 0), (-2, 1), (1, -2)],
     [(-1, 0), (2, 0), (-1, -2), (2, 1)]),

    ([(-1, 0), (2, 0), (-1, -2), (2, 1)],
     [(2, 0), (-1, 0), (2, -1), (-1, 2)]),

    ([(2, 0), (-1, 0), (2, -1), (-1, 2)],
     [(1, 0), (-2, 0), (1, 2), (-2, -1)]),

    ([(1, 0), (-2, 0), (1, 2), (-2, -1)],
     [(-2, 0), (1, 0), (-2, 1), (1, -2)])]

SHAPE_COLORS = [
    None,
    (0, 255, 255),  # cyan
    (0, 0, 255),  # blue
    (255, 165, 0),  # orange
    (255, 255, 0),  # yellow
    (0, 255, 0),  # green
    (128, 0, 128),  # purple
    (255, 0, 0)]  # red

# We could have used simple matrix rotation for rotating the pieces
# but than we would have to calculate anchor, width and height
# on every rotation while maintaining the pivot centered.

SHAPE_I = Shape(
    [ShapeGrid(0, 1, 4, 1,
               [[0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]),
     ShapeGrid(2, 0, 1, 4,
               [[0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]]),
     ShapeGrid(0, 2, 4, 1,
               [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0]]),
     ShapeGrid(1, 0, 1, 4,
               [[0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]])],
    WALL_KICKS_I)

SHAPE_J = Shape(
    [ShapeGrid(0, 0, 3, 2,
               [[2, 0, 0],
                [2, 2, 2],
                [0, 0, 0]]),
     ShapeGrid(1, 0, 2, 3,
               [[0, 2, 2],
                [0, 2, 0],
                [0, 2, 0]]),
     ShapeGrid(0, 1, 3, 2,
               [[0, 0, 0],
                [2, 2, 2],
                [0, 0, 2]]),
     ShapeGrid(0, 0, 2, 3,
               [[0, 2, 0],
                [0, 2, 0],
                [2, 2, 0]])],
    WALL_KICKS_JLSTZ)

SHAPE_L = Shape(
    [ShapeGrid(0, 0, 3, 2,
               [[0, 0, 3],
                [3, 3, 3],
                [0, 0, 0]]),
     ShapeGrid(1, 0, 2, 3,
               [[0, 3, 0],
                [0, 3, 0],
                [0, 3, 3]]),
     ShapeGrid(0, 1, 3, 2,
               [[0, 0, 0],
                [3, 3, 3],
                [3, 0, 0]]),
     ShapeGrid(0, 0, 2, 3,
               [[3, 3, 0],
                [0, 3, 0],
                [0, 3, 0]])],
    WALL_KICKS_JLSTZ)

SHAPE_O = Shape(
    [ShapeGrid(0, 0, 2, 2,
               [[4, 4],
                [4, 4]])],
    [])

SHAPE_S = Shape(
    [ShapeGrid(0, 0, 3, 2,
               [[0, 5, 5],
                [5, 5, 0],
                [0, 0, 0]]),
     ShapeGrid(1, 0, 2, 3,
               [[0, 5, 0],
                [0, 5, 5],
                [0, 0, 5]]),
     ShapeGrid(0, 1, 3, 2,
               [[0, 0, 0],
                [0, 5, 5],
                [5, 5, 0]]),
     ShapeGrid(0, 0, 2, 3,
               [[5, 0, 0],
                [5, 5, 0],
                [0, 5, 0]])],
    WALL_KICKS_JLSTZ)

SHAPE_T = Shape(
    [ShapeGrid(0, 0, 3, 2,
               [[0, 6, 0],
                [6, 6, 6],
                [0, 0, 0]]),
     ShapeGrid(1, 0, 2, 3,
               [[0, 6, 0],
                [0, 6, 6],
                [0, 6, 0]]),
     ShapeGrid(0, 1, 3, 2,
               [[0, 0, 0],
                [6, 6, 6],
                [0, 6, 0]]),
     ShapeGrid(0, 0, 2, 3,
               [[0, 6, 0],
                [6, 6, 0],
                [0, 6, 0]])],
    WALL_KICKS_JLSTZ)

SHAPE_Z = Shape(
    [ShapeGrid(0, 0, 3, 2,
               [[7, 7, 0],
                [0, 7, 7],
                [0, 0, 0]]),
     ShapeGrid(1, 0, 2, 3,
               [[0, 0, 7],
                [0, 7, 7],
                [0, 7, 0]]),
     ShapeGrid(0, 1, 3, 2,
               [[0, 0, 0],
                [7, 7, 0],
                [0, 7, 7]]),
     ShapeGrid(0, 0, 2, 3,
               [[0, 7, 0],
                [7, 7, 0],
                [7, 0, 0]])],
    WALL_KICKS_JLSTZ)

SHAPES = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_T, SHAPE_Z]
