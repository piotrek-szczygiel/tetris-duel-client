from collections import Callable
from enum import Enum

import config
from shape import Shape, ShapeGrid


class Direction(Enum):
    cw = 0
    ccw = 1


class Piece:
    def __init__(self, shape: Shape) -> None:
        self.shape = shape
        self.rotation = 0
        self.x = config.cols // 2 - 2
        self.y = -shape.grid[0].height

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

    def draw(self, x: int, y: int) -> None:
        size = config.size
        self.shape.draw(self.rotation,
                        x + self.x * size,
                        y + self.y * size,
                        size)
