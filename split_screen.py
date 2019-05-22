from random import randint
from typing import Callable, List, Optional

from ctx import ctx
from gameplay import Gameplay
from popup import Popup
from state import State


class SplitScreen(State):
    def __init__(self) -> None:
        self.gameplay1 = Gameplay()
        self.gameplay2 = Gameplay()

        self.popups1: List[Popup] = []
        self.popups2: List[Popup] = []
        self.current_popup1: Optional[Popup] = None
        self.current_popup2: Optional[Popup] = None

        self.finished = False
        self.end_screen = False

    def is_finished(self) -> bool:
        return self.finished

    def initialize(self) -> None:
        self.gameplay1.set_device(ctx.device1)
        self.gameplay1.initialize()

        self.gameplay2.set_device(ctx.device2)
        self.gameplay2.initialize()

    def update(self, switch_state: Callable) -> None:
        if not self.end_screen:
            if self.gameplay1.game_over and not self.gameplay2.game_over:
                self.gameplay2.game_over = True
                self.end_screen = True
                self.popups1.append(
                    Popup("You lost!", color="red", gcolor="orange")
                )
                self.popups2.append(
                    Popup("You won!", color="green", gcolor="yellow")
                )
            elif self.gameplay2.game_over and not self.gameplay1.game_over:
                self.gameplay1.game_over = True
                self.end_screen = True
                self.popups1.append(
                    Popup("You won!", color="green", gcolor="yellow")
                )
                self.popups2.append(
                    Popup("You lost!", color="red", gcolor="orange")
                )
            elif self.gameplay1.game_over and self.gameplay2.game_over:
                self.end_screen = True
                self.popups1.append(Popup("Draw!", color="cyan"))
                self.popups2.append(Popup("Draw!", color="cyan"))

        if self.gameplay1.cancel or self.gameplay2.cancel:
            if self.end_screen or self.gameplay1.countdown > 0:
                self.finished = True
                return
            else:
                self.gameplay1.game_over = self.gameplay1.cancel
                self.gameplay2.game_over = self.gameplay2.cancel
                self.gameplay1.cancel = False
                self.gameplay2.cancel = False

        self.gameplay1.update()
        self.gameplay2.update()

        if self.gameplay1.score.duel_lines > 0:
            hole = randint(0, 9)
            self.gameplay2.add_garbage(hole, self.gameplay1.score.duel_lines)
            self.gameplay1.score.duel_lines = 0

        if self.gameplay2.score.duel_lines > 0:
            hole = randint(0, 9)
            self.gameplay1.add_garbage(hole, self.gameplay2.score.duel_lines)
            self.gameplay2.score.duel_lines = 0

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
        self.gameplay1.draw(130, 80)
        self.gameplay2.draw(880, 80)

        if self.current_popup1:
            self.current_popup1.draw(130 + 155, 80 + 220)

        if self.current_popup2:
            self.current_popup2.draw(880 + 155, 80 + 220)
