from typing import Callable, List, Optional

from pygame.locals import *

import ctx
import shape
from bag import Bag
from input import Input
from matrix import Matrix
from piece import Piece
from t_spin import TSpin
from text import Text


class Gameplay:
    def __init__(self) -> None:
        self.matrix = Matrix()
        self.bag = Bag()
        self.piece: Optional[Piece] = None
        self.input = Input()

        self.holder: Optional[Piece] = None
        self.hold_lock = False

        self.game_over = False

        self.last_fall: float
        self.fall_interval = 1.0

        self.last_lock_cancel: float

        self.t_spin = False
        self.rows_to_clear: List[int] = []

    def is_over(self) -> bool:
        return self.game_over

    def get_matrix(self) -> Matrix:
        return self.matrix

    def get_piece(self) -> Piece:
        return self.piece

    def get_bag(self) -> Bag:
        return self.bag

    def get_holder(self) -> Piece:
        return self.holder

    def initialize(self) -> None:
        self.input.subscribe_list(
            [
                (K_DOWN, self.action_down, True),
                (K_RIGHT, self.action_right, True),
                (K_LEFT, self.action_left, True),
                (K_UP, self.action_rotate_right),
                (K_x, self.action_rotate_right),
                (K_z, self.action_rotate_left),
                (K_LSHIFT, self.action_soft_fall),
                (K_SPACE, self.action_hard_fall),
                (K_c, self.action_hold),
            ]
        )

        self.new_piece()

    def action_down(self) -> None:
        if self.piece.move(0, 1, self.matrix.collision):
            self.reset_fall()

    def action_right(self) -> None:
        self.piece.move(1, 0, self.matrix.collision)

    def action_left(self) -> None:
        self.piece.move(-1, 0, self.matrix.collision)

    def action_rotate_right(self) -> None:
        self.piece.rotate(self.matrix.collision, clockwise=True)

    def action_rotate_left(self) -> None:
        self.piece.rotate(self.matrix.collision, clockwise=False)

    def action_soft_fall(self) -> None:
        if self.piece.fall(self.matrix.collision) > 0:
            self.reset_fall()

    def action_hard_fall(self) -> None:
        self.piece.fall(self.matrix.collision)
        self.lock_piece()

    def action_hold(self) -> None:
        self.hold()

    def new_piece(self) -> None:
        self.piece = self.bag.take()
        self.reset_piece()
        if self.matrix.collision(self.piece):
            self.game_over = True

    def reset_piece(self) -> None:
        self.piece.reset()

        for rows in range(self.piece.shape.grid[0].height, 0, -1):
            if self.piece.move(0, rows, self.matrix.collision):
                break

        self.reset_fall()

    def reset_fall(self) -> None:
        self.last_fall = ctx.now

    def soft_fall(self) -> None:
        if self.piece.fall(self.matrix.collision) > 0:
            self.reset_fall()

    def hard_fall(self) -> None:
        self.soft_fall()
        self.lock_piece()

    def hold(self) -> None:
        if self.hold_lock:
            return

        self.hold_lock = True
        self.reset_piece()

        if self.holder is not None:
            self.holder, self.piece = self.piece, self.holder
            self.reset_fall()
        else:
            self.holder = self.piece
            self.new_piece()

    def lock_piece(self) -> None:
        self.hold_lock = False
        self.t_spin = False

        if self.matrix.collision(self.piece) or not self.matrix.lock(self.piece):
            self.game_over = True
        else:
            if TSpin.detect(self.matrix, self.piece):
                self.t_spin = True

            self.new_piece()

        if self.game_over:
            return

        rows = self.matrix.get_full_rows()
        if rows:
            self.rows_to_clear = rows

    def update(self, clear_rows: Callable) -> None:
        self.input.update()

        if self.rows_to_clear:
            clear_rows(self.rows_to_clear, self.t_spin)
            self.rows_to_clear = []

        if self.piece.reset_lock:
            self.piece.reset_lock = False
            self.reset_fall()
            self.last_lock_cancel = ctx.now

        if self.piece.check_collision(0, 1, self.matrix.collision):
            if ctx.now - self.last_lock_cancel > 1.0:
                self.lock_piece()

        if ctx.now - self.last_fall > self.fall_interval:
            if self.piece.move(0, 1, self.matrix.collision):
                self.reset_fall()

    def draw(self, x: int, y: int) -> None:
        self.matrix.draw(x, y)

        if self.piece:
            self.matrix.get_ghost(self.piece).draw(x, y)
            self.piece.draw(x, y)

        self.bag.draw(x + 340, y + 70)

        if self.holder is not None:
            holder_x = x - 65 - self.holder.shape.get_width(0) * 11.25
            self.holder.shape.draw(0, holder_x, y + 60, 22.5, 1.0)
        else:
            shape.SHAPE_HOLD_NONE.draw(0, x - 75, y + 60, 22.5, 1.0)

        Text.draw("Hold", (x - 110, y + 20))
        Text.draw("Next", (x + 315, y + 20))
