import os
import time

import pygame as pg

import config
from ctx import ctx
import ptext
import resources
from main_menu import MainMenu
from marathon import Marathon
from mixer import Mixer
from split_screen import SplitScreen
from state import State
from text import Text


class Main:
    def __init__(self) -> None:
        self.display: pg.Surface
        self.state: State
        self.last_size = config.window_size

    def switch_state(self, state: str) -> None:
        if state == "Duel":
            self.state = SplitScreen()
        elif state == "Marathon":
            self.state = Marathon()
        elif state == "MainMenu":
            self.state = MainMenu()

        self.state.initialize()

    def handle_events(self) -> bool:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ctx.running = False
                return False
            elif event.type == pg.VIDEORESIZE:
                w, h = event.dict["size"]
                old_w, old_h = self.last_size

                if h != old_h:
                    w = int(config.window_size[0] / config.window_size[1] * h)
                else:
                    h = int(config.window_size[1] / config.window_size[0] * w)

                self.display = pg.display.set_mode((w, h), pg.RESIZABLE)
                self.last_size = w, h
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.switch_state("MainMenu")
                elif event.key == pg.K_q:
                    ctx.running = False
                    return False

        return True

    def run(self) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "center"

        ctx.mixer = Mixer()
        ctx.mixer.initialize()

        pg.init()

        self.display = pg.display.set_mode(config.window_size, pg.RESIZABLE)
        ctx.surface = pg.Surface(config.window_size)
        ptext.FONT_NAME_TEMPLATE = resources.path("%s.ttf")

        pg.display.set_caption("Tetris Duel")
        self.switch_state("MainMenu")

        fps_clock = pg.time.Clock()
        while ctx.running:
            if not self.handle_events():
                return

            ctx.now = time.monotonic()
            self.state.update(self.switch_state)

            ctx.surface.fill(pg.Color(config.background))
            self.state.draw()

            fps = "FPS: " + "{0:.1f}".format(fps_clock.get_fps())
            Text.draw(fps, (10, 10), size=2, alpha=0.5, color="gray")

            pg.transform.scale(
                ctx.surface, self.display.get_size(), self.display
            )
            pg.display.flip()
            fps_clock.tick(60)


if __name__ == "__main__":
    Main().run()
