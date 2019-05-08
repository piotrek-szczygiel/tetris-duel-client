import pygame as pg
from mixer import Mixer


class Ctx:
    def __init__(self) -> None:
        self.running = True
        self.now: float

        self.surface: pg.surface.Surface
        self.mixer: Mixer


ctx = Ctx()
