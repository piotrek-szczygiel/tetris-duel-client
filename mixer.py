from typing import Dict

import pygame as pg

from resources import path


class Mixer:
    def __init__(self) -> None:
        self.sounds: Dict[str, pg.mixer.Sound] = {}

    def initialize(self):
        pg.mixer.init(44100, -16, 2, 1024)

        for name in [
            "change",
            "choose",
            "countdown",
            "erase1",
            "erase2",
            "erase3",
            "erase4",
            "gameover",
            "garbage",
            "go",
            "hard_fall",
            "hold",
            "hold_fail",
            "line_fall",
            "lock_warning",
            "main_theme",
            "move",
            "rotate",
            "soft_fall",
        ]:
            self.load_sound(name, name + ".wav")
            self.sounds[name].set_volume(0.1)

    def load_sound(self, name: str, filename: str):
        self.sounds[name] = pg.mixer.Sound(path(filename))

    def play(self, sound: str) -> None:
        if sound in self.sounds:
            self.sounds[sound].play()
