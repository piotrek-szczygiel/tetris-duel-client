from typing import Callable

from ctx import ctx
from input import Input
from state import State
from text import Text
from device import Device
import config
from device_prompter import DevicePrompter
from marathon import Marathon
from split_screen import SplitScreen
from online import Online


class MainMenu(State):
    def __init__(self) -> None:
        self.input1 = Input(Device(config.device1))
        self.input2 = Input(Device(config.device2))

        self.position = 0
        self.min_position = 0
        self.max_position = 3

        self.entered = False

    def is_finished(self) -> bool:
        return False

    def initialize(self) -> None:
        ctx.mixer.play_music("menu_theme")
        binds = {
            "down": self.position_down,
            "up": self.position_up,
            "select": self.position_enter,
            "hard_fall": self.position_enter,
        }
        self.input1.bind(binds)
        self.input2.bind(binds)

    def position_down(self) -> None:
        self.position += 1
        if self.position > self.max_position:
            self.position = self.max_position
        else:
            ctx.mixer.play("change")

    def position_up(self) -> None:
        self.position -= 1
        if self.position < self.min_position:
            self.position = self.min_position
        else:
            ctx.mixer.play("change")

    def position_enter(self) -> None:
        ctx.mixer.play("choose")
        self.entered = True

    def update(self, switch_state: Callable) -> None:
        self.input1.update()
        self.input2.update()

        if self.entered:
            if self.position == 0:
                switch_state(DevicePrompter(Marathon(), 1))
            elif self.position == 1:
                switch_state(DevicePrompter(SplitScreen(), 2))
            elif self.position == 2:
                switch_state(DevicePrompter(Online(), 1))
            elif self.position == 3:
                ctx.running = False

    def draw(self) -> None:
        Text.draw("Tetris", centerx=640, top=30, size=10)

        Text.draw(
            "Duel", centerx=650, top=130, size=8, color="red", gcolor="yellow"
        )

        colors = ["white" for _ in range(self.max_position + 1)]
        colors[self.position] = "gold"

        Text.draw("Marathon", centerx=650, top=300, color=colors[0])
        Text.draw("Split Screen", centerx=650, top=350, color=colors[1])
        Text.draw("Duel Online", centerx=650, top=400, color=colors[2])
        Text.draw("Quit", centerx=650, top=450, color=colors[3])

        x = 460
        y = 305 + self.position * 50
        Text.draw("\u2192", (x, y), color="gold", size=2)
