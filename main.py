import os
import time

import pygame as pg

import config
import ctx
import resources
from game import Game
from state import State


class Main:
    def __init__(self) -> None:
        self.display: pg.Surface
        self.state: State
        self.last_size = config.window_size

    def switch_state(self, state: State) -> None:
        self.state = state
        self.state.initialize()

    def handle_events(self) -> bool:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ctx.running = False
                return False
            elif event.type == pg.VIDEORESIZE:
                w, h = event.dict['size']
                old_w, old_h = self.last_size

                if h != old_h:
                    w = int(config.window_size[0] / config.window_size[1] * h)
                else:
                    h = int(config.window_size[1] / config.window_size[0] * w)

                ctx.display = pg.display.set_mode((w, h), pg.RESIZABLE)
                self.last_size = w, h
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F12:
                    self.switch_state(Game())
                elif event.key == pg.K_q:
                    ctx.running = False
                    return False

        return True

    def run(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
        pg.init()

        self.display = pg.display.set_mode(config.window_size, pg.RESIZABLE)
        ctx.surface = pg.Surface(config.window_size)

        pg.display.set_caption('Tetris Duel')

        ctx.font = pg.font.Font(resources.path('tetris.ttf'), 24)
        ctx.debug_font = pg.font.Font(resources.path('tetris.ttf'), 16)

        self.switch_state(Game())

        fps_clock = pg.time.Clock()
        while ctx.running:
            if not self.handle_events():
                return

            if not self.state.is_running():
                self.switch_state(Game())

            ctx.now = time.monotonic()
            self.state.update()

            ctx.surface.fill(config.background)
            self.state.draw()

            fps = 'FPS: ' + "{0:.1f}".format(fps_clock.get_fps())
            fps_text = ctx.debug_font.render(fps, True, (255, 255, 255))
            ctx.surface.blit(fps_text, (5, 5))

            pg.transform.scale(ctx.surface, self.display.get_size(), self.display)
            pg.display.flip()

            fps_clock.tick(120)


if __name__ == '__main__':
    Main().run()
