from collections import Callable

import config
from movement import Movement
from shape import Shape, ShapeGrid


class Piece:
    def __init__(
            self, shape: Shape, rotation: int = 0, x: int = 0, y: int = 0, ghost=False
    ) -> None:
        self.shape = shape
        self.ghost = ghost
        self.rotation = rotation
        self.x = x
        self.y = y
        self.last_movement = Movement.none
        self.cancel_lock = False

    def reset(self) -> None:
        self.rotation = 0
        self.x = config.cols // 2 - (self.shape.grid[0].width + 1) // 2
        self.y = config.rows - self.shape.grid[0].height - self.shape.grid[0].y
        self.last_movement = Movement.none

    def get_height(self) -> int:
        return self.shape.get_height(self.rotation)

    def move(self, x: int, y: int, collision: Callable) -> bool:
        if self.check_collision(x, y, collision):
            return False

        self.x += x
        self.y += y
        self.last_movement = Movement.move

        if self.check_collision(0, 1, collision):
            self.cancel_lock = True

        return True

    def check_collision(self, x: int, y: int, collision: Callable) -> bool:
        self.x += x
        self.y += y

        result = collision(self)

        self.x -= x
        self.y -= y

        return result

    def rotate(self, clockwise: bool, collision: Callable) -> bool:
        last_rotation = self.rotation
        if self.shape.kicks:
            all_kicks = self.shape.kicks[self.rotation]
        else:
            all_kicks = ([], [])

        if clockwise:
            kicks = all_kicks[0]
            self.rotation += 1
        else:
            kicks = all_kicks[1]
            self.rotation -= 1

        rotation_count = self.shape.get_rotations()

        if self.rotation < 0:
            self.rotation = rotation_count - 1
        elif self.rotation >= rotation_count:
            self.rotation = 0

        rotated = False

        if not collision(self):
            self.last_movement = Movement.rotate
            rotated = True
        else:
            for kick in kicks:
                if self.move(kick[0], kick[1], collision):
                    self.last_movement = Movement.rotate
                    rotated = True
                    break

        if rotated:
            if self.check_collision(0, 1, collision):
                self.cancel_lock = True
            return True
        else:
            self.rotation = last_rotation
            return False

    def get_grid(self) -> ShapeGrid:
        return self.shape.grid[self.rotation]

    def fall(self, collision: Callable) -> int:
        counter = 0
        while self.move(0, 1, collision):
            counter += 1

        if counter > 0:
            self.last_movement = Movement.move

        return counter

    def draw(self, x: int, y: int) -> None:
        size = config.size
        if self.ghost:
            alpha = 0.3
        else:
            alpha = 1.0

        self.shape.draw(
            self.rotation,
            x + self.x * size,
            y + (self.y - config.rows) * size,
            size,
            alpha,
        )
