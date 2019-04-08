import time
from typing import Optional

from pygame.locals import *

import config
import ctx
from bag import Bag
from input import Input
from matrix import Matrix
from piece import Piece
from state import State


class Game(State):
    def __init__(self) -> None:
        self.matrix = Matrix()
        self.bag = Bag()
        self.piece = self.bag.take()
        self.input = Input()

        self.last_fall = time.monotonic()
        self.fall_interval = 1.0

        self.holder: Optional[Piece] = None
        self.hold_lock = False

        collision = self.matrix.collision
        bind = self.input.subscribe
        bind(K_DOWN, True, self.move_down)
        bind(K_RIGHT, True, lambda: self.piece.move(1, 0, collision))
        bind(K_LEFT, True, lambda: self.piece.move(-1, 0, collision))
        bind(K_x, False, lambda: self.piece.rotate(True, collision))
        bind(K_z, False, lambda: self.piece.rotate(False, collision))
        bind(K_SPACE, False, self.hard_fall)
        bind(K_s, False, self.soft_fall)
        bind(K_c, False, self.hold)
        bind(K_r, False, self.debug_new_piece)

    def debug_new_piece(self) -> None:
        self.piece = self.bag.take()
        self.reset_fall()

    def reset_fall(self) -> None:
        self.last_fall = time.monotonic()

    def hold(self) -> None:
        if self.hold_lock:
            return

        self.hold_lock = True
        self.piece.reset()

        if self.holder is not None:
            self.holder, self.piece = self.piece, self.holder
        else:
            self.holder = self.piece
            self.piece = self.bag.take()

        self.reset_fall()

    def move_down(self) -> None:
        if self.piece.move(0, 1, self.matrix.collision):
            self.reset_fall()

    def soft_fall(self) -> None:
        if self.piece.fall(self.matrix.collision) > 0:
            self.reset_fall()

    def hard_fall(self) -> None:
        self.piece.fall(self.matrix.collision)
        self.lock_and_new()

    def lock_and_new(self) -> None:
        self.hold_lock = False
        if not self.matrix.lock(self.piece):
            ctx.running = False
        else:
            self.piece = self.bag.take()
            self.reset_fall()

    def update(self) -> None:
        self.input.update()

        if time.monotonic() - self.last_fall > self.fall_interval:
            if not self.piece.move(0, 1, self.matrix.collision):
                self.lock_and_new()
            else:
                self.reset_fall()

    def draw(self) -> None:
        self.matrix.draw(170, 100)
        self.piece.draw(170, 100)
        self.bag.draw(550, 150)

        if self.holder is not None:
            self.holder.shape.draw(0, 50, 150, config.size * 0.75, 1.0)
