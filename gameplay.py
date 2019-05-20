from typing import List, Optional
from pygame.locals import (
    K_ESCAPE,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_UP,
    K_x,
    K_z,
    K_LSHIFT,
    K_SPACE,
    K_c,
)

import shape
from bag import Bag
from ctx import ctx
from matrix import Matrix
from piece import Piece
from popup import Popup
from score import Score
from t_spin import TSpin
from text import Text

from input import (
    Input,
    DPAD_RIGHT,
    DPAD_LEFT,
    DPAD_DOWN,
    BUTTON_RIGHT,
    BUTTON_DOWN,
    BUTTON_LEFT,
    TRIGGER_LEFT,
    TRIGGER_RIGHT,
    BUTTON_SELECT,
)


class Gameplay:
    def __init__(self, device) -> None:
        self.device = device

        self.matrix = Matrix()
        self.bag = Bag()
        self.piece: Piece
        self.score = Score()
        self.input = Input(device)
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

        self.last_lock_cancel: float
        self.touched_floor = False
        self.movement_counter = 0
        self.movement_locked = False
        self.movement_locked_warning = False

        self.t_spin = False

        self.clearing = False
        self.clearing_rows: List[int] = []
        self.clearing_last: float

        self.garbage_adding = False
        self.garbage_hole = 0
        self.garbage_left = 0
        self.garbage_last: float

        self.send = False

    def is_over(self) -> bool:
        return self.game_over

    def set_over(self) -> None:
        self.game_over = True

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
        if self.device == Input.KEYBOARD:
            self.input.subscribe_list(
                [
                    (K_ESCAPE, self.action_quit),
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
        elif self.device in (Input.JOYSTICK1, Input.JOYSTICK2):
            self.input.subscribe_list(
                [
                    (BUTTON_SELECT, self.action_quit),
                    (DPAD_DOWN, self.action_down, True),
                    (DPAD_RIGHT, self.action_right, True),
                    (DPAD_LEFT, self.action_left, True),
                    (TRIGGER_RIGHT, self.action_rotate_right),
                    (TRIGGER_LEFT, self.action_rotate_left),
                    (BUTTON_RIGHT, self.action_soft_fall),
                    (BUTTON_DOWN, self.action_hard_fall),
                    (BUTTON_LEFT, self.action_hold),
                ]
            )

        self.new_piece()

    def action_quit(self) -> None:
        self.game_over = True
        self.send = True

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
        self.reset_piece()

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
        self.last_lock_cancel = ctx.now

        self.touched_floor = False
        self.movement_locked = False
        self.movement_locked_warning = False

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
        if self.clearing:
            if ctx.now - self.clearing_last > 0.02:
                self.send = True
                self.matrix.collapse_row(self.clearing_rows.pop(0))
                self.clearing_last = ctx.now
                ctx.mixer.play("line_fall")

                if not self.clearing_rows:
                    self.clearing = False
        elif self.garbage_adding:
            if ctx.now - self.garbage_last > 0.03:
                self.send = True
                self.matrix.add_garbage(self.garbage_hole)
                self.garbage_last = ctx.now
                ctx.mixer.play("garbage")
                self.garbage_left -= 1

                if self.garbage_left == 0:
                    self.garbage_adding = False

        if self.game_over:
            self.send = True
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

        if not self.movement_locked:
            self.input.update()

            if self.piece.movement_counter != self.last_piece_movement_counter:
                self.send = True

            self.last_piece_movement_counter = self.piece.movement_counter

        if self.piece.touching_floor and not self.movement_locked:
            if not self.touched_floor:
                self.touched_floor = True
                self.movement_counter = -1
                self.piece.movement_counter = 0

            if self.movement_counter != self.piece.movement_counter:
                self.movement_counter = self.piece.movement_counter
                self.reset_fall()
                self.last_lock_cancel = ctx.now

                if (
                    self.piece.movement_counter >= 15
                    and not self.movement_locked_warning
                ):
                    self.send = True
                    self.movement_locked_warning = True
                    self.popups.append(
                        Popup(
                            "Lock warning!",
                            duration=0.5,
                            size=4,
                            color="orange",
                            gcolor="darkred",
                        )
                    )
                    ctx.mixer.play("lock_warning")

                elif self.piece.movement_counter >= 30:
                    self.send = True

                    self.movement_locked = True
                    self.popups.append(
                        Popup(
                            "Locked!",
                            duration=1.0,
                            color="darkred",
                            gcolor="black",
                        )
                    )

        if self.piece.check_collision(0, 1, self.matrix.collision):
            if ctx.now - self.last_lock_cancel > 1.0:
                self.send = True
                self.lock_piece()

        if ctx.now - self.last_fall > self.fall_interval:
            if self.piece.move(0, 1, self.matrix.collision):
                self.send = True
                self.reset_fall()

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
