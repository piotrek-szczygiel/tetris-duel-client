from typing import Callable, Dict, List, Tuple, Optional

import pygame as pg

import config
from ctx import ctx

Key = int

DPAD_RIGHT = 0
DPAD_LEFT = 1
DPAD_DOWN = 2
DPAD_UP = 3

BUTTON_UP = 4
BUTTON_RIGHT = 5
BUTTON_DOWN = 6
BUTTON_LEFT = 7

TRIGGER_LEFT = 8
TRIGGER_RIGHT = 9

BUTTON_SELECT = 12
BUTTON_START = 13


class Input:
    KEYBOARD = 0
    JOYSTICK1 = 1
    JOYSTICK2 = 2

    def __init__(self, device) -> None:
        self.device = device
        self.joystick: Optional[pg.joystick.Joystick] = None

        joystick_count = pg.joystick.get_count()
        if self.device == Input.JOYSTICK1:
            if joystick_count < 1:
                raise Exception("Joystick 1 is not available")
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()

        elif self.device == Input.JOYSTICK2:
            if joystick_count < 2:
                raise Exception("Joystick 2 is not available")
            self.joystick = pg.joystick.Joystick(1)
            self.joystick.init()

        self.pressed_keys: List[Key] = list()
        self.last_press: Dict[Key, float] = dict()
        self.last_repeat: Dict[Key, float] = dict()

        self.subscriptions: Dict[Key, Tuple[bool, Callable]] = dict()

    def subscribe(self, key: Key, callback: Callable, repeat=False) -> None:
        self.subscriptions[key] = (repeat, callback)

    def subscribe_list(self, binds: List[Tuple]) -> None:
        for bind in binds:
            self.subscribe(*bind)

    def update(self) -> None:
        if self.device == Input.KEYBOARD:
            self.pressed_keys = pg.key.get_pressed()
        elif self.device == Input.JOYSTICK1 or self.device == Input.JOYSTICK2:
            buttons = self.joystick.get_numbuttons()
            self.pressed_keys = [False for _ in range(buttons + 4)]

            for button in range(self.joystick.get_numbuttons()):
                if self.joystick.get_button(button) == 1:
                    self.pressed_keys[button + 4] = True

            if self.joystick.get_numaxes() >= 1:
                value = self.joystick.get_axis(0)
                if value > 0.5:
                    self.pressed_keys[DPAD_RIGHT] = True
                if value < -0.5:
                    self.pressed_keys[DPAD_LEFT] = True

            if self.joystick.get_numaxes() >= 2:
                value = self.joystick.get_axis(1)
                if value > 0.5:
                    self.pressed_keys[DPAD_DOWN] = True
                if value < -0.5:
                    self.pressed_keys[DPAD_UP] = True

        for key, (repeat, callback) in self.subscriptions.items():
            if self.key_pressed(key, repeat):
                callback()

    def key_pressed(self, key: Key, repeat: bool) -> bool:
        if not self.pressed_keys[key]:
            if key in self.last_press:
                del self.last_press[key]
            if key in self.last_repeat:
                del self.last_repeat[key]
            return False

        if key not in self.last_press:
            self.last_press[key] = ctx.now
            return True

        if not repeat:
            return False

        if ctx.now - self.last_press[key] < config.key_repeat_delay:
            return False

        if key not in self.last_repeat:
            self.last_repeat[key] = ctx.now
            return True

        if ctx.now - self.last_repeat[key] < config.key_repeat_interval:
            return False

        self.last_repeat[key] = ctx.now
        return True
