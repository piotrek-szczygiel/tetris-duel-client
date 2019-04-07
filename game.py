from pygame.locals import *

from bag import Bag
from input import Input
from matrix import Matrix
from state import State


class Game(State):
    def __init__(self) -> None:
        self.matrix = Matrix()
        self.bag = Bag()
        self.piece = self.bag.take()
        self.input = Input()

        bind = self.input.subscribe
        collision = self.matrix.collision
        bind(K_DOWN, True, lambda: self.piece.move(0, 1, collision))
        bind(K_RIGHT, True, lambda: self.piece.move(1, 0, collision))
        bind(K_LEFT, True, lambda: self.piece.move(-1, 0, collision))
        bind(K_x, False, lambda: self.piece.rotate(True, collision))
        bind(K_z, False, lambda: self.piece.rotate(False, collision))
        bind(K_s, False, self.lock_and_new)
        bind(K_r, False, self.new_piece)

    def new_piece(self):
        self.piece = self.bag.take()

    def lock_and_new(self):
        self.matrix.lock(self.piece)
        self.piece = self.bag.take()

    def update(self) -> None:
        self.input.update()

    def draw(self) -> None:
        self.matrix.draw(10, 50)
        self.piece.draw(10, 50)
