from random import randint
from typing import Callable, List, Optional

import pygame as pg

import config
from gameplay import Gameplay
from popup import Popup
from state import State


class Online(State):
    def __init__(self) -> None:
        self.gameplay1 = Gameplay(config.input_player1)
        self.gameplay2 = Gameplay(config.input_player2)

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

        self.done = False
        self.game_over = False

    def is_done(self) -> bool:
        return self.done

    def initialize(self) -> None:
        self.gameplay1.initialize()
        self.gameplay2.initialize()

    def update(self, switch_state: Callable) -> None:
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

        self.gameplay1.update()
        self.gameplay2.update()

        if not self.game_over:
            if self.gameplay1.is_over() and not self.gameplay2.is_over():
                self.gameplay2.set_over()
                self.game_over = True
                self.popups1.append(
                    Popup(
                        "You lost!", duration=5.0, color="red", gcolor="orange"
                    )
                )
                self.popups2.append(
                    Popup(
                        "You won!",
                        duration=5.0,
                        color="green",
                        gcolor="yellow",
                    )
                )
            elif self.gameplay2.is_over() and not self.gameplay1.is_over():
                self.gameplay1.set_over()
                self.game_over = True
                self.popups1.append(
                    Popup(
                        "You won!",
                        duration=5.0,
                        color="green",
                        gcolor="yellow",
                    )
                )
                self.popups2.append(
                    Popup(
                        "You lost!", duration=5.0, color="red", gcolor="orange"
                    )
                )
            elif self.gameplay1.is_over() and self.gameplay2.is_over():
                self.game_over = True
                self.popups1.append(Popup("Draw!", duration=5.0, color="cyan"))
                self.popups2.append(Popup("Draw!", duration=5.0, color="cyan"))
        elif (
            self.game_over
            and not self.current_popup1
            and not self.current_popup2
        ):
            self.done = True

        self.popups1.extend(self.gameplay1.get_popups())
        self.gameplay1.clear_popups()

        self.popups2.extend(self.gameplay2.get_popups())
        self.gameplay2.clear_popups()

        if self.gameplay1.score.duel_lines > 0:
            hole = randint(0, 9)
            self.gameplay2.add_garbage(hole, self.gameplay1.score.duel_lines)
            self.gameplay1.score.duel_lines = 0

        if self.gameplay2.score.duel_lines > 0:
            hole = randint(0, 9)
            self.gameplay1.add_garbage(hole, self.gameplay2.score.duel_lines)
            self.gameplay2.score.duel_lines = 0

    def draw(self) -> None:
        self.gameplay1.draw(130, 80)
        self.gameplay2.draw(880, 80)

        if self.current_popup1:
            self.current_popup1.draw(130 + 155, 80 + 220)

        if self.current_popup2:
            self.current_popup2.draw(880 + 155, 80 + 220)
