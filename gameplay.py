from typing import List, Optional
import shape
from bag import Bag
from ctx import ctx
from matrix import Matrix
from piece import Piece
from popup import Popup
from score import Score
from t_spin import TSpin
from text import Text
from input import Input
from device import Device


class Gameplay:
    def __init__(self, device: Device) -> None:
        self.matrix = Matrix()
        self.bag = Bag()
        self.piece: Piece
        self.score = Score()
        self.input = Input(device)
        self.cancel_input = Input(device)

        self.popups: List[Popup] = []

        self.holder: Optional[Piece] = None
        self.hold_lock = False

        self.level = 1

        self.countdown = 3
        self.countdown_last = ctx.now - 1.0
        self.game_over = False

        self.last_fall: float
        self.fall_interval = 1.0

        self.last_piece_movement_counter = 0

        self.t_spin = False

        self.clearing = False
        self.clearing_rows: List[int] = []
        self.clearing_last: float

        self.garbage_adding = False
        self.garbage_hole = 0
        self.garbage_left = 0
        self.garbage_last: float

        self.send = False
        self.cancel = False

    def get_matrix(self) -> Matrix:
        return self.matrix

    def get_piece(self) -> Piece:
        return self.piece

    def get_bag(self) -> Bag:
        return self.bag

    def get_popups(self) -> List[Popup]:
        return self.popups

    def clear_popups(self) -> None:
        self.popups = []

    def initialize(self) -> None:
        self.input.bind(
            {
                "down": self.action_down,
                "right": self.action_right,
                "left": self.action_left,
                "rotate_right": self.action_rotate_right,
                "rotate_left": self.action_rotate_left,
                "soft_fall": self.action_soft_fall,
                "hard_fall": self.action_hard_fall,
                "hold": self.action_hold,
            }
        )

        self.cancel_input.bind({"cancel": self.action_cancel})

        self.new_piece()

    def action_cancel(self) -> None:
        self.cancel = True

    def action_down(self) -> None:
        if self.piece.move(0, 1, self.matrix.collision):
            self.reset_fall()
            ctx.mixer.play("move")

    def action_right(self) -> None:
        if self.piece.move(1, 0, self.matrix.collision):
            ctx.mixer.play("move")
            if self.piece.touching_floor:
                self.reset_fall()

    def action_left(self) -> None:
        if self.piece.move(-1, 0, self.matrix.collision):
            ctx.mixer.play("move")
            if self.piece.touching_floor:
                self.reset_fall()

    def action_rotate_right(self) -> None:
        if self.piece.rotate(self.matrix.collision, clockwise=True):
            ctx.mixer.play("rotate")
            if self.piece.touching_floor:
                self.reset_fall()

    def action_rotate_left(self) -> None:
        if self.piece.rotate(self.matrix.collision, clockwise=False):
            ctx.mixer.play("rotate")
            if self.piece.touching_floor:
                self.reset_fall()

    def action_soft_fall(self) -> None:
        rows = self.piece.fall(self.matrix.collision)
        if rows > 0:
            ctx.mixer.play("soft_fall")
            self.reset_fall()
            self.score.update_soft_drop(rows)

    def action_hard_fall(self) -> None:
        rows = self.piece.fall(self.matrix.collision)
        self.lock_piece()
        if rows > 0:
            ctx.mixer.play("hard_fall")
            self.score.update_hard_drop(rows)

    def action_hold(self) -> None:
        if self.hold_lock:
            ctx.mixer.play("hold_fail")
            return

        self.hold_lock = True

        if self.holder is not None:
            self.holder, self.piece = self.piece, self.holder
            self.reset_piece()
        else:
            self.holder = self.piece
            self.new_piece()

        self.send = True
        ctx.mixer.play("hold")

    def new_piece(self) -> None:
        self.send = True
        self.piece = self.bag.take()
        self.piece.reset()
        self.reset_fall()

        if self.matrix.collision(self.piece):
            self.game_over = True

        if self.garbage_left > 0:
            self.garbage_adding = True
            self.garbage_last = ctx.now

    def reset_piece(self) -> None:
        self.piece.reset()

        for rows in range(self.piece.shape.grid[0].height, 0, -1):
            if self.piece.move(0, rows, self.matrix.collision):
                break

        self.reset_fall()

    def reset_fall(self) -> None:
        self.last_fall = ctx.now

    def lock_piece(self) -> None:
        self.hold_lock = False
        self.t_spin = False

        if self.matrix.collision(self.piece) or not self.matrix.lock(
            self.piece
        ):
            self.game_over = True
        else:
            if TSpin.detect(self.matrix, self.piece):
                self.t_spin = True

            self.new_piece()

        if self.game_over:
            return

        rows = self.matrix.get_full_rows()
        if rows:
            popup = self.score.update_clear(self.level, rows, self.t_spin)
            ctx.mixer.play("erase" + str(len(rows)))
            self.clear_rows(rows)
            self.popups.append(popup)

        else:
            self.score.reset_combo()

    def clear_rows(self, rows: List[int]) -> None:
        self.clearing = True
        self.clearing_rows = rows
        self.clearing_last = ctx.now + 0.15

        for row in rows:
            self.matrix.erase_row(row)

    def add_garbage(self, hole: int, count: int) -> None:
        self.garbage_hole = hole
        self.garbage_left = count

    def update(self) -> None:
        self.cancel_input.update()

        if self.clearing:
            if ctx.now - self.clearing_last > 0.02:
                self.send = True
                self.matrix.collapse_row(self.clearing_rows.pop(0))
                self.clearing_last = ctx.now
                ctx.mixer.play("line_fall")

                if not self.clearing_rows:
                    self.clearing = False
                    self.reset_piece()
        elif self.garbage_adding:
            if ctx.now - self.garbage_last > 0.03:
                self.send = True
                self.matrix.add_garbage(self.garbage_hole)
                self.garbage_last = ctx.now
                ctx.mixer.play("garbage")
                self.garbage_left -= 1

                if self.garbage_left == 0:
                    self.garbage_adding = False
                    self.reset_piece()

        if self.game_over:
            return

        if self.countdown >= 0:
            if ctx.now - self.countdown_last > 1.0:
                self.send = True
                self.countdown_last = ctx.now
                ctx.mixer.play("countdown")

                if self.countdown == 0:
                    self.popups.append(
                        Popup("GO!", size=6, color="green", duration=0.4)
                    )

                    ctx.mixer.play("go")
                    ctx.mixer.play_music("main_theme")
                else:
                    self.popups.append(
                        Popup(str(self.countdown), size=6, duration=0.4)
                    )

                self.countdown -= 1
            return

        self.input.update()

        if self.piece.movement_counter != self.last_piece_movement_counter:
            self.send = True

        self.last_piece_movement_counter = self.piece.movement_counter

        if ctx.now - self.last_fall > self.fall_interval:
            self.send = True
            if self.piece.move(0, 1, self.matrix.collision):
                self.reset_fall()
            else:
                self.lock_piece()

    def draw(self, x: int, y: int, draw_piece=True) -> None:
        self.matrix.draw(x, y)

        if draw_piece and self.piece:
            self.matrix.get_ghost(self.piece).draw(x, y)
            self.piece.draw(x, y)

        self.score.draw(x, y - 70)
        self.bag.draw(x + 340, y + 70)

        if self.holder is not None:
            holder_x = int(x - 65 - self.holder.shape.get_width(0) * 11.25)
            self.holder.shape.draw(0, holder_x, y + 60, 22, 1.0)
        else:
            shape.SHAPE_HOLD_NONE.draw(0, x - 85, y + 60, 22, 1.0)

        Text.draw("Hold", centerx=x - 75, top=y + 20)
        Text.draw("Next", centerx=x + 370, top=y + 20)
