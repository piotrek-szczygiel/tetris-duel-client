from collections import Callable
from enum import Enum

from shape import Shape, ShapeGrid


class Direction(Enum):
    cw = 0
    ccw = 1


class Piece:
    def __init__(self, shape: Shape, x: int, y: int) -> None:
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = 0

    def move(self, x: int, y: int, collision: Callable) -> bool:
        self.x += x
        self.y += y

        if collision(self):
            self.x -= x
            self.y -= y
            return False

        return True

    def rotate(self, direction: Direction, collision: Callable) -> bool:
        last_rotation = self.rotation

        if direction == Direction.cw:
            self.rotation = self.rotation + 1 % len(self.shape.grid)
        elif direction == Direction.ccw:
            if self.rotation <= 0:
                self.rotation = len(self.shape.grid) - 1
            else:
                self.rotation = self.rotation - 1

        if collision(self):
            self.rotation = last_rotation
            return False

        return True

    def get_grid(self) -> ShapeGrid:
        return self.shape.grid[self.rotation]

    def draw(self, x: int, y: int, size: int) -> None:
        self.shape.draw(self.rotation, x, y, size, True)
