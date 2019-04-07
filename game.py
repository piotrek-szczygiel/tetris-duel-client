import time

from pygame.locals import *

import ctx
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

        self.last_fall = time.monotonic()
        self.fall_interval = 1.0

        bind = self.input.subscribe
        collision = self.matrix.collision
        bind(K_DOWN, True, self.move_down)
        bind(K_RIGHT, True, lambda: self.piece.move(1, 0, collision))
        bind(K_LEFT, True, lambda: self.piece.move(-1, 0, collision))
        bind(K_x, False, lambda: self.piece.rotate(True, collision))
        bind(K_z, False, lambda: self.piece.rotate(False, collision))
        bind(K_SPACE, False, self.hard_fall)
        bind(K_s, False, self.soft_fall)
        bind(K_r, False, self.debug_new_piece)

    def debug_new_piece(self):
        self.piece = self.bag.take()
        self.last_fall = time.monotonic()

    def move_down(self):
        if self.piece.move(0, 1, self.matrix.collision):
            self.last_fall = time.monotonic()

    def soft_fall(self):
        if self.piece.fall(self.matrix.collision) > 0:
            self.last_fall = time.monotonic()

    def hard_fall(self):
        self.piece.fall(self.matrix.collision)
        self.lock_and_new()

    def lock_and_new(self):
        if not self.matrix.lock(self.piece):
            ctx.running = False
        else:
            self.piece = self.bag.take()
            self.last_fall = time.monotonic()

    def update(self) -> None:
        self.input.update()
        now = time.monotonic()

        if now - self.last_fall > self.fall_interval:
            if not self.piece.move(0, 1, self.matrix.collision):
                self.lock_and_new()
            else:
                self.last_fall = now

    def draw(self) -> None:
        self.matrix.draw(70, 70)
        self.piece.draw(70, 70)
