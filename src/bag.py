from collections import deque

import random

from src.piece import PIECES


class Bag:
    def __init__(self):
        self.bag = deque(maxlen=14)

    def initialize(self):
        for _ in range(2):
            self.fill_half()

    def fill_half(self):
        pieces = list(PIECES.values())
        random.shuffle(pieces)
        for piece in pieces:
            self.bag.append(piece)

    def pop_tetromino(self):
        if len(self.bag) == 7:
            self.fill_half()

        return self.bag.pop()

    def show(self, elements=7):
        return list(self.bag)[:elements]
