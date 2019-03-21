import pygame
from blinker import signal

from colors import BACKGROUND_RGB


class Renderer:
    def __init__(self):
        self.display = None

    def initialize_display(self):
        self.display = pygame.display.set_mode((1500, 1000))
        pygame.display.set_caption("Tetris")

    def tick(self, brain):
        brain.board.render()

        self.display.fill(BACKGROUND_RGB)
        self.display.blit(brain.board.surface, (0, 0))

        if brain.piece:
            brain.piece.render()

        pygame.display.flip()
