from collections import Callable

import config
from shape import Shape, ShapeGrid, WallKicks


class Piece:
    def __init__(self, shape: Shape, shadow=False) -> None:
        self.shape = shape
        self.shadow = shadow
        self.rotation = 0
        self.x = 0
        self.y = 0
        self.reset()

    def reset(self) -> None:
        # spawn the new piece in the 'left middle'
        self.rotation = 0
        self.x = config.cols // 2 - (self.shape.grid[0].width + 1) // 2
        self.y = config.rows - self.shape.grid[0].height - self.shape.grid[0].y

    def move(self, x: int, y: int, collision: Callable) -> bool:
        self.x += x
        self.y += y

        if collision(self):
            self.x -= x
            self.y -= y
            return False

        return True

    def rotate(self, clockwise: bool, collision: Callable) -> bool:
        last_rotation = self.rotation
        if self.shape.wall_kicks:
            wall_kicks: WallKicks = self.shape.wall_kicks[self.rotation]
        else:
            wall_kicks = ([], [])

        if clockwise:
            kicks = wall_kicks[0]
            self.rotation += 1
        else:
            kicks = wall_kicks[1]
            self.rotation -= 1

        rotation_count = len(self.shape.grid)

        if self.rotation < 0:
            self.rotation = rotation_count - 1
        elif self.rotation >= rotation_count:
            self.rotation = 0

        if not collision(self):
            return True

        for kick in kicks:
            if self.move(kick[0], kick[1], collision):
                return True

        self.rotation = last_rotation
        return False

    def get_grid(self) -> ShapeGrid:
        return self.shape.grid[self.rotation]

    def fall(self, collision: Callable) -> int:
        counter = 0
        while self.move(0, 1, collision):
            counter += 1

        return counter

    def draw(self, x: int, y: int) -> None:
        size = config.size
        if self.shadow:
            ratio = 0.5
        else:
            ratio = 1.0

        self.shape.draw(self.rotation,
                        x + self.x * size,
                        y + (self.y - config.rows) * size,
                        size,
                        ratio)
