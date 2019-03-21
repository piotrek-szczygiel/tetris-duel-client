from time import monotonic

from blinker import signal

from bag import Bag
from board import Board


class Brain:
    def __init__(self):
        self.bag = Bag()
        self.board = Board()

        self.piece = None
        self.last_fall = None

    def new_piece(self):
        self.last_fall = monotonic()
        self.piece = self.bag.pop_piece()
        self.piece.board_x = 0
        self.piece.board_y = 0

    def tick(self):
        now = monotonic()

        if now - self.last_fall > 1.0:
            self.last_fall = now
            self.piece.board_y += 1
