from typing import Callable, Optional, List

import pygame as pg
from pygame.locals import *

import config
from ctx import ctx
from gameplay import Gameplay
from input import Input
from popup import Popup
from state import State
from text import Text


class Marathon(State):
    def __init__(self) -> None:
        self.input = Input(Input.KEYBOARD)
        self.gameplay = Gameplay(config.input_player1)

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

        self.goal = 5

        self.text_hold: pg.Surface
        self.text_next: pg.Surface

        self.popups: List[Popup] = []
        self.current_popup: Optional[Popup] = None

        self.popup_game_over = False

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
        if not self.current_popup and self.popups:
            self.current_popup = self.popups.pop(0)
            self.current_popup.duration *= 2
        elif self.current_popup:
            if not self.current_popup.update():
                self.current_popup = None

        if not self.gameplay.is_over():
            self.input.update()
        elif not self.popup_game_over:
            self.popup_game_over = True
            self.popups.append(Popup("Game over!", duration=3.0, color="red"))

        self.gameplay.update()

        self.popups.extend(self.gameplay.get_popups())
        self.gameplay.clear_popups()

        if self.gameplay.score.lines > 0:
            self.goal -= self.gameplay.score.lines
            self.goal = max(0, self.goal)
            self.gameplay.score.lines = 0

            if self.goal == 0:
                if self.gameplay.level == 15 and not self.popup_game_over:
                    self.popup_game_over = True
                    self.popups.append(
                        Popup("You won!", duration=3.0, color="green", gcolor="yellow")
                    )
                    self.gameplay.set_over()
                else:
                    self.gameplay.score.lines_cleared = 0
                    self.gameplay.level += 1
                    self.goal = 5 * self.gameplay.level
                    self.gameplay.fall_interval = self.gravity[self.gameplay.level - 1]

    def draw(self) -> None:
        self.gameplay.draw(200, 80)

        Text().draw("Level", centerx=125, top=300)
        Text().draw(
            str(self.gameplay.level), centerx=125, top=340, size=4, color="gold"
        )

        Text().draw("Goal", centerx=125, top=450)
        Text().draw(str(self.goal), centerx=125, top=490, size=4, color="green")

        if self.current_popup:
            self.current_popup.draw(650, 250, center=False)
