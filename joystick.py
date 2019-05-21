from typing import Dict, List, Tuple
import pygame as pg
from ctx import ctx
import config

Button = int
Axis = int
Direction = int
Bind = Tuple[str, bool]


class Joystick:
    def __init__(self, joystick: pg.joystick) -> None:
        self.joystick = joystick

        self.pressed_buttons: List[bool] = list()
        self.last_button_press: Dict[Button, float] = dict()
        self.last_button_repeat: Dict[Button, float] = dict()

        self.axes: List[Direction] = list()
        self.last_axis_press: Dict[Tuple[Axis, Direction], float] = dict()
        self.last_axis_repeat: Dict[Tuple[Axis, Direction], float] = dict()

        self.button_binds: Dict[Button, Bind] = dict()
        self.axes_binds: Dict[Tuple[Axis, Direction], Bind] = dict()

    def bind_button(self, button: Button, action: str, repeat=False) -> None:
        self.button_binds[button] = (action, repeat)

    def bind_axis(
        self, axis: Axis, direction: Direction, action: str, repeat=False
    ) -> None:
        self.axes_binds[(axis, direction)] = (action, repeat)

    def update(self) -> List[str]:
        actions: List[str] = list()

        num_buttons = self.joystick.get_numbuttons()

        self.pressed_buttons = [False for _ in range(num_buttons)]
        for button in range(num_buttons):
            self.pressed_buttons[button] = (
                self.joystick.get_button(button) == 1
            )

        num_axes = self.joystick.get_numaxes()

        self.pressed_axes = [0 for _ in range(num_axes)]
        for axis in range(num_axes):
            value = self.joystick.get_axis(axis)

            if value > 0.5:
                self.pressed_axes[axis] = 1
            elif value < 0.5:
                self.pressed_axes[axis] = -1
            else:
                self.pressed_axes[axis] = 0

        for button, (action, repeat) in self.button_binds.items():
            if self.button_pressed(button, repeat):
                actions += [action]

        for (axis, direction), (action, repeat) in self.axes_binds.items():
            if self.axis_pressed(axis, direction, repeat):
                actions += [action]

        return actions

    def button_pressed(self, button: Button, repeat: bool) -> bool:
        if not self.pressed_buttons[button]:
            if button in self.last_button_press:
                del self.last_button_press[button]
            if button in self.last_button_repeat:
                del self.last_button_repeat[button]
            return False

        if button not in self.last_button_press:
            self.last_button_press[button] = ctx.now
            return True

        if not repeat:
            return False

        if ctx.now - self.last_button_press[button] < config.key_repeat_delay:
            return False

        if button not in self.last_button_repeat:
            self.last_button_repeat[button] = ctx.now
            return True

        if (
            ctx.now - self.last_button_repeat[button]
            < config.key_repeat_interval
        ):
            return False

        self.last_button_repeat[button] = ctx.now
        return True

    def axis_pressed(
        self, axis: Axis, direction: Direction, repeat: bool
    ) -> bool:
        if self.pressed_axes[axis] != direction:
            if (axis, direction) in self.last_axis_press:
                del self.last_axis_press[(axis, direction)]
            if (axis, direction) in self.last_axis_repeat:
                del self.last_axis_repeat[(axis, direction)]
            return False

        if (axis, direction) not in self.last_axis_press:
            self.last_axis_press[(axis, direction)] = ctx.now
            return True

        if not repeat:
            return False

        if (
            ctx.now - self.last_axis_press[(axis, direction)]
            < config.key_repeat_delay
        ):
            return False

        if (axis, direction) not in self.last_axis_repeat:
            self.last_axis_repeat[(axis, direction)] = ctx.now
            return True

        if (
            ctx.now - self.last_axis_repeat[(axis, direction)]
            < config.key_repeat_interval
        ):
            return False

        self.last_axis_repeat[(axis, direction)] = ctx.now
        return True
