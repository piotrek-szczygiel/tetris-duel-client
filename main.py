import os

import pygame
from pygame.locals import *

import config
import ctx
from game import Game
from state import State


class Main:
    def __init__(self) -> None:
        self.display = None
        self.state: State = Game()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == QUIT:
                ctx.running = False
                return False
            elif event.type == VIDEORESIZE:
                ctx.display = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            elif event.type == KEYDOWN:
                if event.key == K_F12:
                    self.state = Game()
                elif event.key == K_q:
                    ctx.running = False
                    return False

        return True

    def run(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
        pygame.init()
        self.display = pygame.display.set_mode(config.window_size, HWSURFACE | RESIZABLE)
        ctx.surface = pygame.Surface(config.window_size, HWSURFACE)
        pygame.display.set_caption('Tetris Duel')

        fps_clock = pygame.time.Clock()
        while ctx.running:
            if not self.handle_events():
                return

            self.state.update()

            ctx.surface.fill(config.background)
            self.state.draw()

            pygame.transform.scale(ctx.surface, self.display.get_size(), self.display)
            pygame.display.flip()

            fps_clock.tick(120)


if __name__ == '__main__':
    Main().run()
