from bag import Bag
from matrix import Matrix
from state import State


class Game(State):
    def __init__(self) -> None:
        self.matrix = Matrix()
        self.bag: Bag

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.matrix.draw(10, 10)
