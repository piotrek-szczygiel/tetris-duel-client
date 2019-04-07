import config
from bag import Bag
from matrix import Matrix
from piece import Piece
from state import State


class Game(State):
    def __init__(self) -> None:
        self.matrix = Matrix()
        self.bag = Bag()
        self.piece = Piece(self.bag.take(), 0, 0)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.matrix.draw(10, 10)
        self.piece.draw(10, 10, config.size)
