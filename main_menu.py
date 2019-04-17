from typing import Callable

from pygame.locals import *

import ctx
from input import Input
from state import State
from text import Text


class MainMenu(State):
    def __init__(self) -> None:
        self.input = Input()

        self.position = 0
        self.min_position = 0
        self.max_position = 2

        self.entered = False

    def initialize(self) -> None:
        self.input.subscribe_list(
            [
                (K_DOWN, self.position_down),
                (K_UP, self.position_up),
                (K_RETURN, self.position_enter),
            ]
        )

    def position_down(self) -> None:
        self.position = min(self.max_position, self.position + 1)

    def position_up(self) -> None:
        self.position = max(self.min_position, self.position - 1)

    def position_enter(self) -> None:
        self.entered = True

    def update(self, switch_state: Callable) -> None:
        self.entered = False
        self.input.update()

        if self.entered:
            if self.position == 0:
                switch_state("Duel")
            elif self.position == 1:
                switch_state("Single")
            elif self.position == 2:
                ctx.running = False

    def draw(self) -> None:
        Text.draw("Tetris", centerx=640, top=30, size=10)

        Text.draw("Duel", centerx=650, top=130, size=8, color="red", gcolor="yellow")

        colors = [None, None, None]
        colors[self.position] = "palegreen"

        Text.draw("Duel", centerx=650, top=300, size=4, color=colors[0])
        Text.draw("Single", centerx=650, top=370, size=4, color=colors[1])
        Text.draw("Quit", centerx=650, top=440, size=4, color=colors[2])

        x = 490
        y = 303 + self.position * 70
        Text.draw("\u2192", (x, y), color="gold")
