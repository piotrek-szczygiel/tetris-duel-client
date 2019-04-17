from typing import Callable, List, Optional

import pygame as pg
from pygame.locals import *

import ctx
import shape
from gameplay import Gameplay
from input import Input
from popup import Popup
from state import State
from text import Text


class Duel(State):
    def __init__(self) -> None:
        self.input = Input()

        self.gameplay1 = Gameplay()
        self.gameplay2 = Gameplay()

        self.clearing = False
        self.clearing_rows: List[int] = []
        self.clearing_last: float

        self.ending = False

        self.text_hold: pg.Surface
        self.text_next: pg.Surface

        self.popup1: Optional[Popup] = None
        self.popup2: Optional[Popup] = None

    def initialize(self) -> None:
        self.gameplay1.initialize()

        self.input.subscribe_list(
            [
                (K_r, self.debug_new_piece),
                (K_p, self.debug_pause),
                (K_t, self.debug_t_spin_tower),
                (K_g, self.debug_garbage),
            ]
        )

    def debug_pause(self) -> None:
        self.pause = not self.pause

    def debug_new_piece(self) -> None:
        self.gameplay1.new_piece()

    def debug_t_spin_tower(self) -> None:
        self.gameplay1.get_matrix().debug_tower()
        self.gameplay1.new_piece()

    def debug_garbage(self) -> None:
        self.gameplay1.get_matrix().add_garbage(5)

    def clear_rows(self, rows: List[int], t_spin: bool) -> None:
        self.clearing = True
        self.clearing_rows = rows
        self.clearing_last = ctx.now + 0.15

        for row in rows:
            self.gameplay1.get_matrix().empty_row(row)

        row_count = len(rows)

        message = None
        gcolor = pg.Color("black")
        if t_spin:
            gcolor = pg.Color("purple")
            message = "T-Spin"
        elif row_count == 4:
            gcolor = pg.Color("cyan")
            message = "TETRIS"

        if message:
            self.popup1 = Popup(message, gcolor=gcolor)
        else:
            self.popup1 = None

    def update(self, switch_state: Callable) -> None:
        self.input.update()
        self.gameplay1.update(self.clear_rows)

        if self.gameplay1.is_over() and not self.ending:
            self.popup1 = Popup("Game over", duration=3.0, gcolor=pg.Color("darkred"))
            self.ending = True

        if self.clearing and ctx.now - self.clearing_last > 0.02:
            self.gameplay1.get_matrix().collapse_row(self.clearing_rows.pop(0))
            self.clearing_last = ctx.now

            if not self.clearing_rows:
                self.clearing = False

        if self.popup1 and not self.popup1.update():
            self.popup1 = None

            if self.gameplay1.is_over() and self.ending:
                switch_state("MainMenu")

    def draw(self) -> None:
        self.draw_gameplay(self.gameplay1, 120, 80)
        self.draw_gameplay(self.gameplay2, 820, 80)

        if self.popup1:
            self.popup1.draw(120, 80)

        if self.popup2:
            self.popup2.draw(820, 80)

    @staticmethod
    def draw_gameplay(gameplay: Gameplay, x: int, y: int) -> None:
        matrix = gameplay.get_matrix()
        piece = gameplay.get_piece()
        bag = gameplay.get_bag()
        holder = gameplay.get_holder()

        matrix.draw(x, y)

        if piece:
            matrix.get_ghost(piece).draw(x, y)
            piece.draw(x, y)

        bag.draw(x + 340, y + 70)

        if holder is not None:
            holder_x = x - 65 - holder.shape.get_width(0) * 11.25
            holder.shape.draw(0, holder_x, y + 60, 22.5, 1.0)
        else:
            shape.SHAPE_HOLD_NONE.draw(0, x - 75, y + 60, 22.5, 1.0)

        Text.draw("Hold", (x - 110, y + 20))
        Text.draw("Next", (x + 315, y + 20))
