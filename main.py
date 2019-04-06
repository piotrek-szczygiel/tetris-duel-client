import pygame

import ctx
from game import Game
from state import State

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris Duel')

    ctx.display = pygame.display.set_mode(320, 640)

    game = Game()
    state: State = game

    while ctx.running:
        state.update()
        state.draw()
