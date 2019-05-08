from functools import lru_cache
from typing import Tuple

import pygame as pg
import pygame.gfxdraw

import config
from ctx import ctx

RGB = Tuple[float, float, float]


def color_tint(color: RGB, ratio: float) -> RGB:
    return (
        color[0] + (255 - color[0]) * ratio,
        color[1] + (255 - color[1]) * ratio,
        color[2] + (255 - color[2]) * ratio,
    )


def color_shade(color: RGB, ratio: float) -> RGB:
    return color[0] * ratio, color[1] * ratio, color[2] * ratio


@lru_cache()
def color_get(color: RGB, brightness: float, alpha: float) -> RGB:
    if brightness > 1.0:
        color = color_tint(color, brightness - 1.0)
    else:
        color = color_shade(color, brightness)

    bg = pg.Color(config.background)

    return (
        (1.0 - alpha) * bg.r + alpha * color[0],
        (1.0 - alpha) * bg.g + alpha * color[1],
        (1.0 - alpha) * bg.b + alpha * color[2],
    )


def draw_block(color: str, x: float, y: float, size: float, alpha: float = 1.0) -> None:
    color = pg.Color(color)

    color_rgb = color.r, color.g, color.b
    color_down = color_get(color_rgb, 0.4, alpha)
    color_right = color_get(color_rgb, 0.6, alpha)
    color_middle = color_get(color_rgb, 0.8, alpha)
    color_left = color_get(color_rgb, 1.2, alpha)
    color_up = color_get(color_rgb, 1.7, alpha)

    border = 0.1 * size

    # middle rect
    pygame.draw.rect(ctx.surface, color_middle, pygame.Rect(x, y, size, size))

    # upper trapezoid
    pygame.draw.polygon(
        ctx.surface,
        color_up,
        [
            (x, y),
            (x + border, y + border),
            (x + size - border, y + border),
            (x + size, y),
        ],
    )

    # left trapezoid
    pygame.draw.polygon(
        ctx.surface,
        color_left,
        [
            (x, y + size),
            (x + border, y + size - border),
            (x + border, y + border),
            (x, y),
        ],
    )

    # right trapezoid
    pygame.draw.polygon(
        ctx.surface,
        color_right,
        [
            (x + size, y + size),
            (x + size - border, y + size - border),
            (x + size - border, y + border),
            (x + size, y),
        ],
    )

    # lower trapezoid
    pygame.draw.polygon(
        ctx.surface,
        color_down,
        [
            (x, y + size),
            (x + border, y + size - border),
            (x + size - border, y + size - border),
            (x + size, y + size),
        ],
    )
