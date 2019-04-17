from typing import Tuple

import pygame as pg

import _ptext
import ctx

Position = Tuple[int, int]


class Text:
    @staticmethod
    def draw(
        *args, size=3, color="white", gcolor="white", **kwargs
    ) -> Tuple[pg.Surface, Position]:
        return _ptext.draw(
            *args,
            fontname="tetris",
            fontsize=8 * size,
            color=color,
            gcolor=gcolor,
            surf=ctx.surface,
            **kwargs
        )
