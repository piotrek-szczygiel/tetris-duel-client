from typing import Callable, Optional

import pygame as pg
from pygame.locals import *

import ctx
from gameplay import Gameplay
from input import Input
from popup import Popup
from state import State


class Marathon(State):
    def __init__(self) -> None:
        self.input = Input()
        self.gameplay = Gameplay()

        self.ending = False

        self.gravity = [
            1.00000,
            0.79300,
            0.61780,
            0.47273,
            0.35520,
            0.26200,
            0.18968,
            0.13473,
            0.09388,
            0.06415,
            0.04298,
            0.02822,
            0.01815,
            0.01144,
            0.00706,
        ]

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
        ctx.mixer.play("garbage")

    def update(self, switch_state: Callable) -> None:
        self.input.update()
        self.gameplay.update()

        popup = self.gameplay.get_popup()
        if popup:
            self.popup = popup

        if self.gameplay.movement_locked:
            self.popup = Popup("Locked!", duration=1.0, color="darkred", gcolor="black")

        if self.gameplay.is_over() and not self.ending:
            self.popup = Popup("Game over", duration=3.0, gcolor="darkred")
            self.ending = True

        if self.popup and not self.popup.update():
            self.popup = None

            if self.gameplay.is_over() and self.ending:
                switch_state("MainMenu")

    def draw(self) -> None:
        self.gameplay.draw(490, 80)

        if self.popup:
            self.popup.draw(250, 250)
