from pygame.locals import *

from input import *
from state import State
from text import Text


class MainMenu(State):
    def __init__(self) -> None:
        self.input = Input(config.input_player1)

        self.position = 0
        self.min_position = 0
        self.max_position = 2

        self.entered = False

    def initialize(self) -> None:
        if config.input_player1 == Input.KEYBOARD:
            self.input.subscribe_list(
                [
                    (K_DOWN, self.position_down),
                    (K_UP, self.position_up),
                    (K_RETURN, self.position_enter),
                ]
            )
        else:
            self.input.subscribe_list(
                [
                    (DPAD_DOWN, self.position_down),
                    (DPAD_UP, self.position_up),
                    (BUTTON_DOWN, self.position_enter),
                    (BUTTON_START, self.position_enter),
                ]
            )

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
        self.entered = False
        self.input.update()

        if self.entered:
            if self.position == 0:
                switch_state("Marathon")
            elif self.position == 1:
                switch_state("Duel")
            elif self.position == 2:
                ctx.running = False

    def draw(self) -> None:
        Text.draw("Tetris", centerx=640, top=30, size=10)

        Text.draw("Duel", centerx=650, top=130, size=8, color="red", gcolor="yellow")

        colors = ["white" for _ in range(self.max_position + 1)]
        colors[self.position] = "gold"

        Text.draw("Marathon", centerx=650, top=300, color=colors[0])
        Text.draw("Split Screen", centerx=650, top=350, color=colors[1])
        Text.draw("Quit", centerx=650, top=400, color=colors[2])

        x = 460
        y = 305 + self.position * 50
        Text.draw("\u2192", (x, y), color="gold", size=2)
