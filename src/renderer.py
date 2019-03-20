import pygame


class Renderer:
    def __init__(self):
        self.display = None

    def initialize(self):
        self.display = pygame.display.set_mode((1500, 1000))
        pygame.display.set_caption("Tetris")
