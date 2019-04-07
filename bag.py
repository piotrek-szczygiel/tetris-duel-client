import random
from typing import List

from piece import Piece
from shape import Shape, SHAPES


class Bag:
    def __init__(self) -> None:
        self.bag: List[Shape] = []
        self._fill()

    def take(self) -> Piece:
        shape = self.bag.pop(0)
        self._fill()
        return Piece(shape)

    def peek(self, n: int) -> List[Shape]:
        return self.bag[:n]

    def _fill(self) -> None:
        if len(self.bag) == 0:
            self._add_7()
            self._add_7()
        elif len(self.bag) == 7:
            self._add_7()

    def _add_7(self) -> None:
        shapes = SHAPES[:]
        random.shuffle(shapes)
        self.bag.extend(shapes)
