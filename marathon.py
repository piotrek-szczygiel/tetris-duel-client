from typing import Callable, Optional, List

from gameplay import Gameplay
from popup import Popup
from state import State
from text import Text
from device import Device


class Marathon(State):
    def __init__(self, device: Device) -> None:
        self.gameplay = Gameplay(device)

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

        self.popups: List[Popup] = []
        self.current_popup: Optional[Popup] = None

        self.end_screen = False

        self.finished = False
        self.pause = False

    def is_finished(self) -> bool:
        return self.finished

    def initialize(self) -> None:
        self.gameplay.initialize()

    def update(self, switch_state: Callable) -> None:
        if self.gameplay.game_over and not self.end_screen:
            self.end_screen = True
            self.popups.append(Popup("Game over!", color="red"))

        if self.gameplay.game_over and self.gameplay.cancel:
            self.finished = True
            return

        if self.gameplay.cancel:
            if self.gameplay.countdown > 0:
                self.finished = True
                return
            else:
                self.gameplay.game_over = True
                self.gameplay.cancel = False

        self.gameplay.update()

        if self.gameplay.score.lines > 0:
            self.goal -= self.gameplay.score.lines
            self.goal = max(0, self.goal)
            self.gameplay.score.lines = 0

            if self.goal == 0:
                if self.gameplay.level == 15 and not self.end_screen:
                    self.end_screen = True
                    self.gameplay.game_over = True
                    self.popups.append(
                        Popup("You won!", color="green", gcolor="yellow")
                    )
                else:
                    self.gameplay.level += 1
                    self.goal = 5 * self.gameplay.level
                    self.gameplay.fall_interval = self.gravity[
                        self.gameplay.level - 1
                    ]

        self.popups.extend(self.gameplay.get_popups())
        self.gameplay.clear_popups()

        if not self.current_popup and self.popups:
            self.current_popup = self.popups.pop(0)
            self.current_popup.duration *= 2
        elif self.current_popup:
            if not self.current_popup.update():
                self.current_popup = None

    def draw(self) -> None:
        self.gameplay.draw(200, 80)

        Text().draw("Level", centerx=125, top=300)
        Text().draw(
            str(self.gameplay.level),
            centerx=125,
            top=340,
            size=4,
            color="gold",
        )

        Text().draw("Goal", centerx=125, top=450)
        Text().draw(
            str(self.goal), centerx=125, top=490, size=4, color="green"
        )

        if self.current_popup:
            self.current_popup.draw(650, 250, center=False)
