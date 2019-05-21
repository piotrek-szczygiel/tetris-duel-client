import pygame as pg
import toml
from resources import path


class Device:
    def __init__(self, name: str, joystick_num=0):
        self.name = name

        if name == "dummy":
            self.type = "dummy"
            return

        self.joystick: pg.joystick
        self.joystick_num = joystick_num

        with open(path("controls.toml"), "r") as f:
            self.toml = toml.loads(f.read())[name]

        self.type = self.toml["type"]
        self.actions = self.toml
        del self.actions["type"]

        if self.type == "joystick":
            self.joystick = pg.joystick.Joystick(joystick_num)
            self.joystick.init()
