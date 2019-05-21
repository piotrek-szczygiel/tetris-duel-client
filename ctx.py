import pygame as pg
from mixer import Mixer
from device import Device


class Ctx:
    def __init__(self) -> None:
        self.running = True
        self.now: float

        self.surface: pg.surface.Surface
        self.mixer: Mixer

        self.device1 = Device("dummy")
        self.device2 = Device("dummy")


ctx = Ctx()
