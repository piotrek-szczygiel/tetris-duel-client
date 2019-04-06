from bag import Bag
from matrix import Matrix
from state import State


class Game(State):
    def __init__(self):
        self.matrix = Matrix()
        self.bag: Bag

    def update(self):
        pass

    def draw(self):
        pass
