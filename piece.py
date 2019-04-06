from typing import Tuple

from shape import Shape


class Piece:
    def __init__(self, shape: Shape, x: int, y: int) -> None:
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = 0