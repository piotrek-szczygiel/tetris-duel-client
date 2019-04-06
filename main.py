import pygame

import ctx
from game import Game
from state import State

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris Duel')

    ctx.display = pygame.display.set_mode((320, 640))

    game = Game()
    state: State = game

    while ctx.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ctx.running = False
                break

        state.update()
        state.draw()
