from typing import Tuple

import pygame.gfxdraw

import ctx

RGB = Tuple[float, float, float]
RGBA = Tuple[float, float, float, float]


def color_tint(color: RGB, ratio: float) -> RGB:
    return (
        color[0] + (255 - color[0]) * ratio,
        color[1] + (255 - color[1]) * ratio,
        color[2] + (255 - color[2]) * ratio)


def color_shade(color: RGB, ratio: float) -> RGB:
    return (
        color[0] * ratio,
        color[1] * ratio,
        color[2] * ratio)


def color_alpha(color: RGB, alpha: float) -> RGBA:
    return color[0], color[1], color[2], alpha


def color_get(color: RGB, shade: float, alpha: float) -> RGBA:
    if shade > 1.0:
        return color_alpha(color_tint(color, shade - 1.0), alpha)
    else:
        return color_alpha(color_shade(color, shade), alpha)


def draw_block(color: RGB, x: float, y: float,
               size: float, alpha: float = 255) -> None:
    display = ctx.surface

    color_down = color_get(color, 0.2, alpha)
    color_right = color_get(color, 0.4, alpha)
    color_middle = color_get(color, 0.8, alpha)
    color_left = color_get(color, 1.2, alpha)
    color_up = color_get(color, 1.4, alpha)

    border = 0.125 * size
    # border = 0.0625 * size

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
