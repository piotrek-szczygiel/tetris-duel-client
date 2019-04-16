from random import randint
from typing import List, Optional

import pygame as pg
from pygame.locals import *

import config
import ctx
import shape
from bag import Bag
from input import Input
from matrix import Matrix
from piece import Piece
from state import State
from t_spin import TSpin
from text import Text


class Game(State):
    def __init__(self) -> None:
        self.running = True

        self.matrix = Matrix()
        self.bag = Bag()
        self.piece = self.bag.take()
        self.reset_piece()

        self.input = Input()

        self.last_fall = ctx.now
        self.fall_interval = 1.0

        self.holder: Optional[Piece] = None
        self.hold_lock = False

        self.rows_to_clear: List[int] = []
        self.last_clear = ctx.now

        self.message: Optional[str] = None
        self.message_alpha = 0
        self.message_start = ctx.now
        self.message_duration = 0.0
        self.message_fade = 0.0

        self.garbage_allow = False
        self.garbage_hole = 0
        self.garbage_to_add = 0
        self.garbage_add_last = ctx.now

        self.pause = False
        self.game_over = False

        self.text_hold: pg.Surface
        self.text_next: pg.Surface

    def initialize(self) -> None:
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

    def is_running(self) -> bool:
        return self.running

    def debug_pause(self) -> None:
        self.pause = not self.pause

    def debug_new_piece(self) -> None:
        self.new_piece()

    def add_garbage(self, rows: int) -> None:
        self.garbage_to_add += rows
        self.garbage_hole = randint(0, self.matrix.width - 1)
        self.garbage_add_last = ctx.now

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
        self.last_fall = ctx.now

    def lock_and_new(self) -> None:
        self.hold_lock = False
        t_spin = False

        if self.matrix.collision(self.piece) or not self.matrix.lock(self.piece):
            self.game_over = True
        else:
            if TSpin.detect(self.matrix, self.piece):
                t_spin = True

            self.new_piece()
            self.garbage_allow = True

        if self.game_over:
            return

        rows = self.matrix.get_full_rows()
        if rows:
            row_count = len(rows)
            if t_spin:
                message = "T-spin"
                if row_count == 2:
                    message += " double"
                elif row_count == 3:
                    message += " triple"
            elif row_count == 4:
                message = "Tetris"
            else:
                message = None

            if message is not None:
                self.message = message
                self.message_duration = 0.75
                self.message_fade = 0.3
                self.message_start = ctx.now

            for row in rows:
                self.matrix.empty_row(row)

            self.rows_to_clear = rows
            self.last_clear = ctx.now + 0.15

    def reset_piece(self) -> None:
        self.piece.reset()
        for rows in range(self.piece.shape.grid[0].height, 0, -1):
            if self.piece.move(0, rows, self.matrix.collision):
                break

        self.reset_fall()

    def new_piece(self) -> None:
        self.piece = self.bag.take()
        self.reset_piece()
        if self.matrix.collision(self.piece):
            self.game_over = True

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

    def update(self) -> None:
        if self.rows_to_clear:
            if ctx.now - self.last_clear > 0.02:
                row = self.rows_to_clear.pop(0)
                self.matrix.collapse_row(row)
                self.last_clear = ctx.now

                if not self.rows_to_clear:
                    self.reset_fall()

        if self.garbage_allow and not self.rows_to_clear:
            if self.garbage_to_add > 0 and ctx.now - self.garbage_add_last > 0.05:
                self.matrix.add_garbage(self.garbage_hole)
                self.garbage_to_add -= 1
                self.garbage_add_last = ctx.now

            if self.garbage_to_add == 0:
                self.reset_fall()
                self.garbage_allow = False

        if self.message:
            if ctx.now > self.message_start + self.message_duration:
                self.message = None
                if self.game_over:
                    self.running = False
            elif ctx.now > self.message_start + self.message_duration - self.message_fade:
                self.message_alpha = (
                        1.0
                        - ((ctx.now - self.message_start - self.message_fade) / (
                            self.message_duration - self.message_fade))
                        ** 2
                )
            else:
                self.message_alpha = 255

        self.input.update()

        if self.piece.cancel_lock:
            self.piece.cancel_lock = False
            self.reset_fall()

        if not self.pause and ctx.now - self.last_fall > self.fall_interval:
            if not self.piece.move(0, 1, self.matrix.collision):
                self.lock_and_new()
            else:
                self.reset_fall()

        if self.game_over and not self.message:
            self.message = "Game over"
            self.message_start = ctx.now
            self.message_duration = 1.5
            self.message_fade = 0.75

    def draw(self) -> None:
        board_position = (120, 80)

        self.matrix.draw(*board_position)

        self.matrix.get_ghost(self.piece).draw(*board_position)
        self.piece.draw(*board_position)

        self.bag.draw(440, 150)

        if self.holder is not None:
            x = 55 - self.holder.shape.get_width(0) * config.size * 0.75 / 2
            self.holder.shape.draw(0, x, 140, config.size * 0.75, 1.0)
        else:
            shape.SHAPE_HOLD_NONE.draw(0, 45, 140, config.size * 0.75, 1.0)

        Text.draw("Hold", (10, 100))
        Text.draw("Next", (435, 100))

        if self.message:
            Text.draw(
                self.message,
                centerx=275,
                top=300,
                size=4,
                color=pg.Color("white"),
                alpha=self.message_alpha,
                shadow=(2.0, 2.0),
                scolor=pg.Color("blue"),
            )
