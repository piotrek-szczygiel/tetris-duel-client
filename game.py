from state import State


class Game(State):
    def __init__(self):
        self.board: Board
        self.bag: Bag

    def update(self):
        pass

    def draw(self):
        pass
