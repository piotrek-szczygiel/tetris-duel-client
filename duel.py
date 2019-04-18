from typing import Callable, List, Optional

import pygame as pg
from pygame.locals import *

import ctx
from gameplay import Gameplay
from input import Input
from popup import Popup
from state import State


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

    def clear_rows(self, rows: List[int]) -> None:
        self.clearing = True
        self.clearing_rows = rows
        self.clearing_last = ctx.now + 0.15

        for row in rows:
            self.gameplay1.get_matrix().empty_row(row)

    def update(self, switch_state: Callable) -> None:
        self.input.update()
        message = self.gameplay1.update(self.clear_rows)

        if message:
            self.popup1 = Popup(message, color="gold", gcolor="green", size=4)

        if self.gameplay1.movement_locked:
            self.popup1 = Popup(
                "Locked!", duration=1.0, color="darkred", gcolor="black"
            )

        if self.gameplay1.is_over() and not self.ending:
            self.popup1 = Popup("Game over", duration=3.0, gcolor="darkred")
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
        self.gameplay1.draw(120, 80)
        self.gameplay2.draw(880, 80)

        if self.popup1:
            self.popup1.draw(120 + 155, 80 + 220)

        if self.popup2:
            self.popup2.draw(880 + 155, 80 + 220)
