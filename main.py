import os
from typing import Tuple

import pygame
from pygame.locals import *

import config
import ctx
from game import Game
from state import State


class Main:
    def __init__(self) -> None:
        ctx.display = None
        ctx.surface = None
        self.state: State = Game()

    def initialize_video(self, dimensions: Tuple[int, int]) -> None:
        ctx.display = pygame.display.set_mode(dimensions, RESIZABLE)
        ctx.surface = pygame.Surface(dimensions, SRCALPHA | HWSURFACE)

    def run(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
        pygame.init()
        self.initialize_video((config.width, config.height))
        pygame.display.set_caption('Tetris Duel')
        pygame.mouse.set_visible(False)

        fps_clock = pygame.time.Clock()
        while ctx.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    ctx.running = False
                    break
                elif event.type == VIDEORESIZE:
                    self.initialize_video(event.dict['size'])
                elif event.type == KEYDOWN:
                    if event.key == K_F12:
                        self.state = Game()
                    elif event.key == K_q:
                        ctx.running = False
                        break

            self.state.update()

            ctx.display.fill((0, 0, 32))
            ctx.surface.fill((0, 0, 0, 0))
            self.state.draw()
            ctx.display.blit(ctx.surface, (0, 0))
            pygame.display.flip()
            fps_clock.tick(60)


if __name__ == '__main__':
    Main().run()
