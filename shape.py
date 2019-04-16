from typing import List, Tuple

from block import draw_block

Grid = List[List[int]]
Kicks = Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]


class ShapeGrid:
    def __init__(self, x: int, y: int, width: int, height: int, grid: Grid) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.grid = grid


class Shape:
    def __init__(self, name: str, grid: List[ShapeGrid], kicks: List[Kicks]) -> None:
        self.name = name
        self.grid = grid
        self.kicks = kicks

    def get_width(self, rotation: int) -> int:
        return len(self.grid[rotation].grid[0])

    def get_height(self, rotation: int) -> int:
        return len(self.grid[rotation].grid)

    def get_rotations(self) -> int:
        return len(self.grid)

    def draw(self, rotation: int, x: int, y: int, size: int, ratio: float) -> None:
        grid = self.grid[rotation]
        width, height = self.get_width(rotation), self.get_height(rotation)

        for my in range(height):
            for mx in range(width):
                c = grid.grid[my][mx]
                if c == 0:
                    continue

                draw_block(SHAPE_COLORS[c], x + mx * size, y + my * size, size, ratio)


# https://harddrop.com/wiki/SRS

KICKS_JLSTZ = [
    ([(-1, 0), (-1, -1), (0, 2), (-1, 2)], [(1, 0), (1, -1), (0, 2), (1, 2)]),
    ([(1, 0), (1, 1), (0, -2), (1, -2)], [(1, 0), (1, 1), (0, -2), (1, -2)]),
    ([(1, 0), (1, -1), (0, 2), (1, 2)], [(-1, 0), (-1, -1), (0, 2), (-1, 2)]),
    ([(-1, 0), (-1, 1), (0, -2), (-1, -2)], [(-1, 0), (-1, 1), (0, -2), (-1, -2)]),
]

KICKS_I = [
    ([(-2, 0), (1, 0), (-2, 1), (1, -2)], [(-1, 0), (2, 0), (-1, -2), (2, 1)]),
    ([(-1, 0), (2, 0), (-1, -2), (2, 1)], [(2, 0), (-1, 0), (2, -1), (-1, 2)]),
    ([(2, 0), (-1, 0), (2, -1), (-1, 2)], [(1, 0), (-2, 0), (1, 2), (-2, -1)]),
    ([(1, 0), (-2, 0), (1, 2), (-2, -1)], [(-2, 0), (1, 0), (-2, 1), (1, -2)]),
]

SHAPE_COLORS = [
    None,
    (0, 255, 255),  # cyan
    (0, 0, 255),  # blue
    (255, 165, 0),  # orange
    (255, 255, 0),  # yellow
    (0, 255, 0),  # green
    (128, 0, 128),  # purple
    (255, 0, 0),  # red
    (224, 224, 224),  # gray
]

GARBAGE_COLOR = 8

# We could have used simple matrix rotation for rotating the pieces
# but than we would have to calculate anchor, width and height
# on every rotation while maintaining the pivot centered.

SHAPE_I = Shape(
    "I",
    [
        ShapeGrid(0, 1, 4, 1, [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
        ShapeGrid(2, 0, 1, 4, [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        ShapeGrid(0, 2, 4, 1, [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        ShapeGrid(1, 0, 1, 4, [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]),
    ],
    KICKS_I,
)

SHAPE_J = Shape(
    "J",
    [
        ShapeGrid(0, 0, 3, 2, [[2, 0, 0], [2, 2, 2], [0, 0, 0]]),
        ShapeGrid(1, 0, 2, 3, [[0, 2, 2], [0, 2, 0], [0, 2, 0]]),
        ShapeGrid(0, 1, 3, 2, [[0, 0, 0], [2, 2, 2], [0, 0, 2]]),
        ShapeGrid(0, 0, 2, 3, [[0, 2, 0], [0, 2, 0], [2, 2, 0]]),
    ],
    KICKS_JLSTZ,
)

SHAPE_L = Shape(
    "L",
    [
        ShapeGrid(0, 0, 3, 2, [[0, 0, 3], [3, 3, 3], [0, 0, 0]]),
        ShapeGrid(1, 0, 2, 3, [[0, 3, 0], [0, 3, 0], [0, 3, 3]]),
        ShapeGrid(0, 1, 3, 2, [[0, 0, 0], [3, 3, 3], [3, 0, 0]]),
        ShapeGrid(0, 0, 2, 3, [[3, 3, 0], [0, 3, 0], [0, 3, 0]]),
    ],
    KICKS_JLSTZ,
)

SHAPE_O = Shape("O", [ShapeGrid(0, 0, 2, 2, [[4, 4], [4, 4]])], [])

SHAPE_S = Shape(
    "S",
    [
        ShapeGrid(0, 0, 3, 2, [[0, 5, 5], [5, 5, 0], [0, 0, 0]]),
        ShapeGrid(1, 0, 2, 3, [[0, 5, 0], [0, 5, 5], [0, 0, 5]]),
        ShapeGrid(0, 1, 3, 2, [[0, 0, 0], [0, 5, 5], [5, 5, 0]]),
        ShapeGrid(0, 0, 2, 3, [[5, 0, 0], [5, 5, 0], [0, 5, 0]]),
    ],
    KICKS_JLSTZ,
)

SHAPE_T = Shape(
    "T",
    [
        ShapeGrid(0, 0, 3, 2, [[0, 6, 0], [6, 6, 6], [0, 0, 0]]),
        ShapeGrid(1, 0, 2, 3, [[0, 6, 0], [0, 6, 6], [0, 6, 0]]),
        ShapeGrid(0, 1, 3, 2, [[0, 0, 0], [6, 6, 6], [0, 6, 0]]),
        ShapeGrid(0, 0, 2, 3, [[0, 6, 0], [6, 6, 0], [0, 6, 0]]),
    ],
    KICKS_JLSTZ,
)

SHAPE_Z = Shape(
    "Z",
    [
        ShapeGrid(0, 0, 3, 2, [[7, 7, 0], [0, 7, 7], [0, 0, 0]]),
        ShapeGrid(1, 0, 2, 3, [[0, 0, 7], [0, 7, 7], [0, 7, 0]]),
        ShapeGrid(0, 1, 3, 2, [[0, 0, 0], [7, 7, 0], [0, 7, 7]]),
        ShapeGrid(0, 0, 2, 3, [[0, 7, 0], [7, 7, 0], [7, 0, 0]]),
    ],
    KICKS_JLSTZ,
)

SHAPE_HOLD_NONE = Shape(".", [ShapeGrid(0, 0, 1, 1, [[8]])], [])

SHAPES = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_T, SHAPE_Z]
