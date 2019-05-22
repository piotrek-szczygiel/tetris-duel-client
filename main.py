import time

import pygame as pg

import ptext
import resources
from config import config
from ctx import ctx
from device import Device
from main_menu import MainMenu
from mixer import Mixer
from state import State
from text import Text


class Main:
    def __init__(self) -> None:
        self.display: pg.Surface
        self.state: State
        self.device1 = Device("dummy")
        self.device2 = Device("dummy")

    def switch_state(self, state: State) -> None:
        ctx.mixer.stop_music()
        self.state = state
        self.state.initialize()

    def handle_events(self) -> bool:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ctx.running = False
                return False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_EQUALS, pg.K_PLUS):
                    w, h = self.display.get_size()
                    w = int(w * 1.1)
                    h = int(h * 1.1)
                    self.display = pg.display.set_mode((w, h))
                elif event.key in (pg.K_MINUS, pg.K_UNDERSCORE):
                    w, h = self.display.get_size()
                    w = int(w * 0.9)
                    h = int(h * 0.9)
                    self.display = pg.display.set_mode((w, h))

        return True

    def run(self) -> None:
        ctx.mixer = Mixer()
        ctx.mixer.initialize()

        pg.init()

        self.display = pg.display.set_mode(config.window_size)
        ctx.surface = pg.Surface(config.window_size)
        ptext.FONT_NAME_TEMPLATE = resources.path("%s.ttf")

        pg.display.set_caption("Tetris Duel")
        self.switch_state(MainMenu())

        fps_clock = pg.time.Clock()
        while ctx.running:
            if not self.handle_events():
                return

            ctx.now = time.monotonic()
            self.state.update(self.switch_state)

            if self.state.is_finished():
                self.switch_state(MainMenu())

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
