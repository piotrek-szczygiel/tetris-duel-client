import time
from typing import Optional

from pygame.locals import *

import config
import ctx
from bag import Bag
from input import Input
from matrix import Matrix
from movement import Movement, TSpin
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

        self.last_movement = Movement.none

        self.pause = False

        self.enemy = Matrix()
        self.enemy.debug_tower()

        collision = self.matrix.collision
        bind = self.input.subscribe
        bind(K_DOWN, True, self.move_down)
        bind(K_RIGHT, True, self.move_right)
        bind(K_LEFT, True, self.move_left)
        bind(K_x, False, self.rotate_right)
        bind(K_z, False, self.rotate_left)
        bind(K_SPACE, False, self.hard_fall)
        bind(K_LSHIFT, False, self.soft_fall)
        bind(K_c, False, self.hold)
        bind(K_r, False, self.debug_new_piece)
        bind(K_p, False, self.debug_pause)
        bind(K_t, False, lambda: self.matrix.debug_tower())

    def debug_pause(self) -> None:
        self.pause = not self.pause

    def move_right(self) -> None:
        self.piece.move(1, 0, self.matrix.collision)
        self.last_movement = Movement.move

    def move_left(self) -> None:
        self.piece.move(-1, 0, self.matrix.collision)
        self.last_movement = Movement.move

    def rotate_right(self) -> None:
        if self.piece.rotate(True, self.matrix.collision):
            self.last_movement = Movement.rotate

    def rotate_left(self) -> None:
        if self.piece.rotate(False, self.matrix.collision):
            self.last_movement = Movement.rotate

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
            self.last_movement = Movement.move

    def soft_fall(self) -> None:
        if self.piece.fall(self.matrix.collision) > 0:
            self.reset_fall()
            self.last_movement = Movement.move

    def hard_fall(self) -> None:
        self.piece.fall(self.matrix.collision)
        self.lock_and_new()

    def debug_new_piece(self) -> None:
        self.piece = self.bag.take()
        self.reset_fall()

    def reset_fall(self) -> None:
        self.last_fall = time.monotonic()
        self.last_movement = Movement.move

    def lock_and_new(self) -> None:
        self.hold_lock = False
        t_spin = False
        if not self.matrix.lock(self.piece):
            ctx.running = False
        else:
            if TSpin.detect(self.matrix, self.piece, self.last_movement):
                t_spin = True
            self.piece = self.bag.take()
            self.reset_fall()

        rows = self.matrix.get_full_rows()
        if rows:
            print('Rows cleared:', len(rows))
            if t_spin:
                print('T-spin!')
            for row in rows:
                self.matrix.clear_row(row)

        self.last_movement = Movement.move

    def update(self) -> None:
        self.input.update()

        if not self.pause and time.monotonic() - self.last_fall > self.fall_interval:
            if not self.piece.move(0, 1, self.matrix.collision):
                self.lock_and_new()
            else:
                self.reset_fall()

    def draw(self) -> None:
        board_position = (170, 100)

        self.matrix.draw(*board_position)
        self.enemy.draw(700, 100)

        self.piece.draw(*board_position)

        ghost = self.matrix.get_ghost(self.piece)
        if ghost is not None:
            ghost.draw(*board_position)

        self.bag.draw(510, 150)

        if self.holder is not None:
            self.holder.shape.draw(0, 80, 150, config.size * 0.75, 255)
