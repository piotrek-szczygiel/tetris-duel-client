import random
from typing import List

import config
from piece import Piece
from shape import Shape, SHAPES


class Bag:
    def __init__(self) -> None:
        self.bag: List[Shape] = list()
        self.fill()

    def take(self) -> Piece:
        shape = self.bag.pop(0)
        self.fill()
        piece = Piece(shape)
        return piece

    def peek(self, n: int) -> List[Shape]:
        return self.bag[:n]

    def fill(self) -> None:
        if len(self.bag) == 0:
            self.add_7()
            self.add_7()
        elif len(self.bag) == 7:
            self.add_7()

    def add_7(self) -> None:
        shapes = SHAPES[:]
        random.shuffle(shapes)
        self.bag.extend(shapes)

    def draw(self, x: int, y: int) -> None:
        bag = self.peek(4)
        size = config.size * 0.75
        gap = size * 4

        for i, shape in enumerate(bag):
            shape.draw(0, x, y + i * gap, size, 1.0)
