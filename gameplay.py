from typing import List, Optional

from pygame.locals import *

import ctx
import shape
from bag import Bag
from input import Input
from matrix import Matrix
from piece import Piece
from popup import Popup
from score import Score
from t_spin import TSpin
from text import Text


class Gameplay:
    def __init__(self) -> None:
        self.matrix = Matrix()
        self.bag = Bag()
        self.piece: Optional[Piece] = None
        self.score = Score()
        self.input = Input()
        self.popup: Optional[Popup] = None

        self.holder: Optional[Piece] = None
        self.hold_lock = False

        self.level = 1

        self.game_over = False

        self.last_fall: float
        self.fall_interval = 1.0

        self.last_lock_cancel: float
        self.touched_floor = False
        self.movement_counter = 0
        self.movement_locked = False

        self.t_spin = False

        self.clearing = False
        self.clearing_rows: List[int] = []
        self.clearing_last: float

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

    def get_popup(self) -> Popup:
        return self.popup

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
            ctx.mixer.play("move")

    def action_right(self) -> None:
        if self.piece.move(1, 0, self.matrix.collision):
            ctx.mixer.play("move")

    def action_left(self) -> None:
        if self.piece.move(-1, 0, self.matrix.collision):
            ctx.mixer.play("move")

    def action_rotate_right(self) -> None:
        if self.piece.rotate(self.matrix.collision, clockwise=True):
            ctx.mixer.play("rotate")

    def action_rotate_left(self) -> None:
        if self.piece.rotate(self.matrix.collision, clockwise=False):
            ctx.mixer.play("rotate")

    def action_soft_fall(self) -> None:
        rows = self.piece.fall(self.matrix.collision)
        if rows > 0:
            ctx.mixer.play("move")
            self.reset_fall()
            self.score.update_soft_drop(rows)

    def action_hard_fall(self) -> None:
        rows = self.piece.fall(self.matrix.collision)
        self.lock_piece()
        if rows > 0:
            ctx.mixer.play("hard_fall")
            self.score.update_hard_drop(rows)

    def action_hold(self) -> None:
        self.hold()

    def new_piece(self) -> None:
        self.piece = self.bag.take()
        self.reset_piece()
        self.touched_floor = False
        self.movement_locked = False
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

    def hold(self) -> None:
        if self.hold_lock:
            ctx.mixer.play("hold_fail")
            return

        self.hold_lock = True
        self.reset_piece()

        if self.holder is not None:
            self.holder, self.piece = self.piece, self.holder
            self.reset_fall()
        else:
            self.holder = self.piece
            self.new_piece()

        ctx.mixer.play("hold")

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
            message = self.score.update_clear(self.level, rows, self.t_spin)
            ctx.mixer.play("erase")
            self.clear_rows(rows)
            self.popup = Popup(message, color="gold", gcolor="green", size=4)

        else:
            self.score.reset_combo()

    def clear_rows(self, rows: List[int]) -> None:
        self.clearing = True
        self.clearing_rows = rows
        self.clearing_last = ctx.now + 0.15

        for row in rows:
            self.matrix.erase_row(row)

    def update(self) -> None:
        if not self.movement_locked:
            self.input.update()

        if self.clearing and ctx.now - self.clearing_last > 0.02:
            self.matrix.collapse_row(self.clearing_rows.pop(0))
            self.clearing_last = ctx.now
            ctx.mixer.play("line_fall")

            if not self.clearing_rows:
                self.clearing = False

        if self.piece.touching_floor and not self.movement_locked:
            if not self.touched_floor:
                self.touched_floor = True
                self.movement_counter = -1
                self.piece.movement_counter = 0

            if self.movement_counter != self.piece.movement_counter:
                if self.piece.movement_counter <= 15:
                    self.movement_counter = self.piece.movement_counter
                    self.reset_fall()
                    self.last_lock_cancel = ctx.now

                    if self.piece.movement_counter == 15:
                        self.movement_locked = True

        if self.movement_locked:
            self.popup = Popup("Locked!", duration=1.0, color="darkred", gcolor="black")

        if self.piece.check_collision(0, 1, self.matrix.collision):
            if ctx.now - self.last_lock_cancel > 1.0:
                self.lock_piece()

        if ctx.now - self.last_fall > self.fall_interval:
            if self.piece.move(0, 1, self.matrix.collision):
                self.reset_fall()

    def draw(self, x: int, y: int) -> None:
        self.score.draw(x, y - 70)
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
