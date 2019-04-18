from typing import Callable, List, Optional

import pygame as pg
from pygame.locals import *

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

        self.popups1: List[Popup] = []
        self.popups2: List[Popup] = []
        self.current_popup1: Optional[Popup] = None
        self.current_popup2: Optional[Popup] = None

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

    def update(self, switch_state: Callable) -> None:
        if self.gameplay1.is_over():
            return

        self.input.update()
        self.gameplay1.update()

        self.popups1.extend(self.gameplay1.get_popups())
        self.gameplay1.clear_popups()

        self.popups2.extend(self.gameplay2.get_popups())
        self.gameplay2.clear_popups()

        if not self.current_popup1 and self.popups1:
            self.current_popup1 = self.popups1.pop(0)
        elif self.current_popup1:
            if not self.current_popup1.update():
                self.current_popup1 = None

        if not self.current_popup2 and self.popups2:
            self.current_popup2 = self.popups2.pop(0)
        elif self.current_popup2:
            if not self.current_popup2.update():
                self.current_popup2 = None

    def draw(self) -> None:
        self.gameplay1.draw(120, 80)
        self.gameplay2.draw(880, 80)

        if self.current_popup1:
            self.current_popup1.draw(120 + 155, 80 + 220)

        if self.current_popup2:
            self.current_popup2.draw(880 + 155, 80 + 220)
