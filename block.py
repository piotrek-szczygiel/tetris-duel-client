from typing import Tuple

import pygame.gfxdraw

import config
import ctx

RGB = Tuple[float, float, float]


def color_tint(color: RGB, ratio: float) -> RGB:
    return (
        color[0] + (255 - color[0]) * ratio,
        color[1] + (255 - color[1]) * ratio,
        color[2] + (255 - color[2]) * ratio,
    )


def color_shade(color: RGB, ratio: float) -> RGB:
    return color[0] * ratio, color[1] * ratio, color[2] * ratio


def color_get(color: RGB, brightness: float, alpha: float) -> RGB:
    if brightness > 1.0:
        color = color_tint(color, brightness - 1.0)
    else:
        color = color_shade(color, brightness)

    bg = config.background

    return (
        (1.0 - alpha) * bg[0] + alpha * color[0],
        (1.0 - alpha) * bg[1] + alpha * color[1],
        (1.0 - alpha) * bg[2] + alpha * color[2],
    )


def draw_block(color: RGB, x: float, y: float, size: float, alpha: float = 1.0) -> None:
    color_down = color_get(color, 0.4, alpha)
    color_right = color_get(color, 0.6, alpha)
    color_middle = color_get(color, 0.8, alpha)
    color_left = color_get(color, 1.2, alpha)
    color_up = color_get(color, 1.8, alpha)

    border = 0.1 * size

    # middle rect
    pygame.gfxdraw.box(ctx.surface, pygame.Rect(x, y, size, size), color_middle)

    # upper trapezoid
    upper_poly = [
        (x, y),
        (x + border, y + border),
        (x + size - border, y + border),
        (x + size, y),
    ]

    pygame.gfxdraw.aapolygon(ctx.surface, upper_poly, color_up)
    pygame.gfxdraw.filled_polygon(ctx.surface, upper_poly, color_up)

    # left trapezoid
    left_poly = [
        (x, y + size),
        (x + border, y + size - border),
        (x + border, y + border),
        (x, y),
    ]

    pygame.gfxdraw.aapolygon(ctx.surface, left_poly, color_left)
    pygame.gfxdraw.filled_polygon(ctx.surface, left_poly, color_left)

    # right trapezoid
    right_poly = [
        (x + size, y + size),
        (x + size - border, y + size - border),
        (x + size - border, y + border),
        (x + size, y),
    ]

    pygame.gfxdraw.aapolygon(ctx.surface, right_poly, color_right)
    pygame.gfxdraw.filled_polygon(ctx.surface, right_poly, color_right)

    # lower trapezoid
    lower_poly = [
        (x, y + size),
        (x + border, y + size - border),
        (x + size - border, y + size - border),
        (x + size, y + size),
    ]

    pygame.gfxdraw.aapolygon(ctx.surface, lower_poly, color_down)
    pygame.gfxdraw.filled_polygon(ctx.surface, lower_poly, color_down)
