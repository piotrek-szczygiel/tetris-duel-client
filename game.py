import time
from typing import List, Optional

from pygame.locals import *

import config
import ctx
from bag import Bag
from input import Input
from matrix import Matrix
from piece import Piece
from state import State
from t_spin import TSpin


class Game(State):
    def __init__(self) -> None:
        self.matrix: Matrix = Matrix()
        self.bag: Bag = Bag()
        self.piece: Piece = self.bag.take()

        self.input: Input = Input()

        self.last_fall: float = time.monotonic()
        self.fall_interval: float = 1.0

        self.holder: Optional[Piece] = None
        self.hold_lock: bool = False

        self.rows_to_clear: List[int] = []
        self.last_clear: float = time.monotonic()

        self.garbage_allow: bool = False
        self.garbage_to_add: int = 0
        self.garbage_add_last: float = time.monotonic()

        self.pause: bool = False
        self.game_over: bool = False

        self.bind_keys()

    def update(self) -> None:
        now = time.monotonic()

        if self.rows_to_clear:
            if now - self.last_clear > 0.02:
                row = self.rows_to_clear.pop(0)
                self.matrix.collapse_row(row)
                self.last_clear = now

                if not self.rows_to_clear:
                    self.reset_fall()

        if self.garbage_allow and self.garbage_to_add > 0:
            if now - self.garbage_add_last > 0.05:
                self.matrix.add_garbage(3)
                self.garbage_to_add -= 1
                self.garbage_add_last = now

                if self.garbage_to_add == 0:
                    self.garbage_allow = False
                    self.reset_fall()

        self.input.update()

        if self.piece.cancel_lock:
            self.piece.cancel_lock = False
            self.reset_fall()

        if not self.pause and now - self.last_fall > self.fall_interval:
            if not self.piece.move(0, 1, self.matrix.collision):
                self.lock_and_new()
            else:
                self.reset_fall()

        if self.game_over:
            print('Game over!')
            ctx.running = False

    def draw(self) -> None:
        board_position = (170, 100)

        self.matrix.draw(*board_position)

        self.matrix.get_ghost(self.piece).draw(*board_position)
        self.piece.draw(*board_position)

        self.bag.draw(510, 150)

        if self.holder is not None:
            self.holder.shape.draw(0, 80, 150, config.size * 0.75, 1.0)

    def bind_keys(self):
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
        bind(K_t, False, self.matrix.debug_tower)
        bind(K_g, False, lambda: self.add_garbage(5))

    def debug_pause(self) -> None:
        self.pause = not self.pause

    def debug_new_piece(self) -> None:
        self.piece = self.bag.take()
        self.reset_fall()

    def add_garbage(self, rows: int) -> None:
        self.garbage_to_add += rows
        self.garbage_add_last = time.monotonic()

    def move_right(self) -> None:
        self.piece.move(1, 0, self.matrix.collision)

    def move_left(self) -> None:
        self.piece.move(-1, 0, self.matrix.collision)

    def move_down(self) -> None:
        if self.piece.move(0, 1, self.matrix.collision):
            self.reset_fall()

    def rotate_right(self) -> None:
        self.piece.rotate(True, self.matrix.collision)

    def rotate_left(self) -> None:
        self.piece.rotate(False, self.matrix.collision)

    def soft_fall(self) -> None:
        if self.piece.fall(self.matrix.collision) > 0:
            self.reset_fall()

    def hard_fall(self) -> None:
        self.piece.fall(self.matrix.collision)
        self.lock_and_new()

    def reset_fall(self) -> None:
        self.last_fall = time.monotonic()

    def lock_and_new(self) -> None:
        self.hold_lock = False
        t_spin = False

        if self.matrix.collision(self.piece) or not self.matrix.lock(self.piece):
            self.game_over = True
        else:
            if TSpin.detect(self.matrix, self.piece):
                t_spin = True
            self.piece = self.bag.take()
            self.reset_fall()
            self.garbage_allow = True

        rows = self.matrix.get_full_rows()
        if rows:
            print('Rows cleared:', len(rows))
            if t_spin:
                print('T-spin!')

            self.rows_to_clear = rows
            self.last_clear = time.monotonic()

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
