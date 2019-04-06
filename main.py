import pygame

import ctx
from game import Game
from state import State

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris Duel')

    ctx.display = pygame.display.set_mode((420, 820))

    game = Game()
    state: State = game

    fps_clock = pygame.time.Clock()
    while ctx.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ctx.running = False
                break

        state.update()

        ctx.display.fill((0, 0, 0))
        state.draw()
        pygame.display.flip()
        fps_clock.tick(60)
