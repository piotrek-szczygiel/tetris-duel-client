from typing import Callable

import pygame as pg
from pygame.locals import *

import ctx
import shape
from input import Input
from state import State
from text import Text


class MainMenu(State):
    def __init__(self) -> None:
        self.input = Input()

        self.position = 1
        self.min_position = 1
        self.max_position = 2
        self.cursor = shape.SHAPE_T

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
                pass
            elif self.position == 1:
                switch_state("Game")
            elif self.position == 2:
                ctx.running = False

    def draw(self) -> None:
        Text.draw("Tetris", centerx=275, top=30, size=6)
        Text.draw(
            "Duel",
            centerx=275,
            top=100,
            size=6,
            color=pg.Color("red"),
            gcolor=pg.Color("yellow"),
        )

        Text.draw("Duel", centerx=275, top=240, color=pg.Color("dimgray"))
        Text.draw("Single", centerx=275, top=300)
        Text.draw("Quit", centerx=275, top=360)

        x = 240 + self.position * 60
        self.cursor.draw(1, 150, x, 8, 1.0)
