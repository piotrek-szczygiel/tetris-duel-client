import pygame as pg

import ctx
from text import Text


class Popup:
    def __init__(
            self,
            text: str,
            duration=1.0,
            size=4,
            color=pg.Color("white"),
            shadow_color=pg.Color("blue"),
    ) -> None:
        self.text = text
        self.duration = duration
        self.size = size
        self.color = color
        self.shadow_color = shadow_color

        self.fade = self.duration / 3
        self.alpha = 1.0

        self.start = ctx.now

    def update(self) -> bool:
        if self.start + self.duration < ctx.now:
            return False

        if self.start + self.duration - self.fade < ctx.now:
            ratio = (ctx.now - self.start - self.fade) / (self.duration - self.fade)
            self.alpha = 1.0 - ratio ** 2

        return True

    def draw(self) -> None:
        Text.draw(
            self.text,
            centerx=275,
            top=300,
            size=self.size,
            color=self.color,
            alpha=self.alpha,
            shadow=(2.0, 2.0),
            scolor=self.shadow_color,
        )
