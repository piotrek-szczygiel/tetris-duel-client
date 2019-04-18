from typing import Callable, List, Optional

import pygame as pg
from pygame.locals import *

import ctx
from gameplay import Gameplay
from input import Input
from popup import Popup
from state import State


class Single(State):
    def __init__(self) -> None:
        self.input = Input()
        self.gameplay = Gameplay()

        self.clearing = False
        self.clearing_rows: List[int] = []
        self.clearing_last: float

        self.ending = False

        self.text_hold: pg.Surface
        self.text_next: pg.Surface

        self.popup: Optional[Popup] = None

    def initialize(self) -> None:
        self.gameplay.initialize()

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
        self.gameplay.new_piece()

    def debug_t_spin_tower(self) -> None:
        self.gameplay.get_matrix().debug_tower()
        self.gameplay.new_piece()

    def debug_garbage(self) -> None:
        self.gameplay.get_matrix().add_garbage(5)

    def clear_rows(self, rows: List[int], t_spin: bool) -> None:
        self.clearing = True
        self.clearing_rows = rows
        self.clearing_last = ctx.now + 0.15

        for row in rows:
            self.gameplay.get_matrix().empty_row(row)

        row_count = len(rows)

        message = None
        gcolor = "black"
        if t_spin:
            gcolor = "purple"
            message = "T-Spin"
        elif row_count == 4:
            gcolor = "cyan"
            message = "TETRIS"

        if message:
            self.popup = Popup(message, gcolor=gcolor)
        else:
            self.popup = None

    def update(self, switch_state: Callable) -> None:
        self.input.update()
        self.gameplay.update(self.clear_rows)

        if self.gameplay.movement_locked and not self.popup:
            self.popup = Popup("Locked!", duration=1.0, color="darkred", gcolor="black")

        if self.gameplay.is_over() and not self.ending:
            self.popup = Popup("Game over", duration=3.0, gcolor="darkred")
            self.ending = True

        if self.clearing and ctx.now - self.clearing_last > 0.02:
            self.gameplay.get_matrix().collapse_row(self.clearing_rows.pop(0))
            self.clearing_last = ctx.now

            if not self.clearing_rows:
                self.clearing = False

        if self.popup and not self.popup.update():
            self.popup = None

            if self.gameplay.is_over() and self.ending:
                switch_state("MainMenu")

    def draw(self) -> None:
        self.gameplay.draw(490, 80)

        if self.popup:
            self.popup.draw(120, 80)
