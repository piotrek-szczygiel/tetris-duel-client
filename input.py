from device import Device
from keyboard import Keyboard
from joystick import Joystick
import pygame as pg
from typing import Dict, Callable, List


class Input:
    def __init__(self, device: Device) -> None:
        self.binds: Dict[str, Callable] = dict()
        if device.type == "keyboard":
            self.type = "keyboard"
            self.keyboard = Keyboard()

            for action, how in device.actions.items():
                if type(how) is str:
                    self.keyboard.bind(Input.str_to_key(how), action)
                elif type(how) is list and "repeat" in how:
                    self.keyboard.bind(Input.str_to_key(how[0]), action, True)
                else:
                    raise Exception("invalid binding: {}".format(how))

        elif device.type == "joystick":
            self.type = "joystick"
            self.joystick = Joystick(device.joystick)

            for action, how in device.actions.items():
                invalid = True
                if type(how) is int:
                    self.joystick.bind_button(how, action)
                    invalid = False
                elif type(how) is list:
                    if (
                        len(how) >= 3
                        and type(how[0]) is str
                        and how[0] == "axis"
                    ):
                        repeat = "repeat" in how
                        axis = int(how[1])

                        direction = 0
                        if how[2] in ("+", "-"):
                            if how[2] == "-":
                                direction = -1
                            elif how[2] == "+":
                                direction = 1
                            invalid = False

                        self.joystick.bind_axis(
                            axis, direction, action, repeat
                        )

                if invalid:
                    raise Exception("invalid binding: {}".format(how))

    def bind(self, binds: Dict[str, Callable]) -> None:
        self.binds = binds

    def update(self) -> None:
        if self.type == "dummy":
            return

        actions: List[str] = list()
        if self.type == "keyboard":
            actions = self.keyboard.update()
        elif self.type == "joystick":
            actions = self.joystick.update()

        for action in actions:
            if action in self.binds:
                self.binds[action]()

    @staticmethod
    def str_to_key(key: str) -> int:
        keys = {
            "esc": pg.K_ESCAPE,
            "enter": pg.K_RETURN,
            "up": pg.K_UP,
            "down": pg.K_DOWN,
            "right": pg.K_RIGHT,
            "left": pg.K_LEFT,
            "x": pg.K_x,
            "z": pg.K_z,
            "lshift": pg.K_LSHIFT,
            "space": pg.K_SPACE,
            "c": pg.K_c,
        }

        if key in keys:
            return keys[key]
        else:
            raise Exception("invalid key: {}".format(key))
