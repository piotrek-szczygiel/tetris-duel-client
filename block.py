from typing import Tuple

import pygame.gfxdraw

import ctx

Color = Tuple[float, float, float]


def color_tint(color: Color, ratio: float) -> Color:
    return (
        color[0] + (255 - color[0]) * ratio,
        color[1] + (255 - color[1]) * ratio,
        color[2] + (255 - color[2]) * ratio)


def color_shade(color: Color, ratio: float) -> Color:
    return (
        color[0] * ratio,
        color[1] * ratio,
        color[2] * ratio)


def draw_block(color: Color, x: float, y: float,
               size: float, highlight=False) -> None:
    display = ctx.display

    if highlight:
        color_down = color_shade(color, 0.4)
        color_right = color_shade(color, 0.5)
        color_middle = color_shade(color, 0.9)
        color_left = color_tint(color, 0.2)
        color_up = color_tint(color, 0.4)
    else:
        color_down = color_shade(color, 0.3)
        color_right = color_shade(color, 0.4)
        color_middle = color_shade(color, 0.8)
        color_left = color_tint(color, 0.1)
        color_up = color_tint(color, 0.3)

    border = 0.0625 * size

    # middle rect
    pygame.gfxdraw.box(
        display,
        pygame.Rect(x, y, size, size),
        color_middle)

    # upper trapezoid
    upper_poly = [
        (x, y),
        (x + border, y + border),
        (x + size - border, y + border),
        (x + size - 1, y)]

    pygame.gfxdraw.aapolygon(display, upper_poly, color_up)
    pygame.gfxdraw.filled_polygon(display, upper_poly, color_up)

    # left trapezoid
    left_poly = [
        (x, y + size - 1),
        (x + border, y + size - border),
        (x + border, y + border),
        (x, y)]

    pygame.gfxdraw.aapolygon(display, left_poly, color_left)
    pygame.gfxdraw.filled_polygon(display, left_poly, color_left)

    # right trapezoid
    right_poly = [
        (x + size - 1, y + size - 1),
        (x + size - border, y + size - border),
        (x + size - border, y + border),
        (x + size - 1, y)]

    pygame.gfxdraw.aapolygon(display, right_poly, color_right)
    pygame.gfxdraw.filled_polygon(display, right_poly, color_right)

    # lower trapezoid
    lower_poly = [
        (x, y + size - 1),
        (x + border, y + size - border),
        (x + size - border, y + size - border),
        (x + size - 1, y + size - 1)]

    pygame.gfxdraw.aapolygon(display, lower_poly, color_down)
    pygame.gfxdraw.filled_polygon(display, lower_poly, color_down)
