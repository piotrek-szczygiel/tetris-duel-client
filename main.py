import os

import pygame
from pygame.locals import *

import config
import ctx
from game import Game

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    pygame.init()
    pygame.display.set_caption('Tetris Duel')
    ctx.display = pygame.display.set_mode((config.width, config.height), RESIZABLE)
    ctx.surface = pygame.Surface((config.width, config.height), SRCALPHA | HWSURFACE)
    pygame.mouse.set_visible(False)

    state = Game()

    fps_clock = pygame.time.Clock()
    while ctx.running:
        for event in pygame.event.get():
            if event.type == QUIT:
                ctx.running = False
                break
            elif event.type == VIDEORESIZE:
                ctx.display = pygame.display.set_mode(event.dict['size'],
                                                      RESIZABLE)
            elif event.type == KEYDOWN:
                if event.key == K_F12:
                    state = Game()
                elif event.key in (K_q, K_ESCAPE):
                    ctx.running = False
                    break

        state.update()

        ctx.display.fill((0, 0, 32))
        ctx.surface.fill((0, 0, 0, 0))
        state.draw()
        ctx.display.blit(ctx.surface, (0, 0))
        pygame.display.flip()
        fps_clock.tick(60)
