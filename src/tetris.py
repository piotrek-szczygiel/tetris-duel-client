import pygame

from src.mixer import Mixer
from src.renderer import Renderer


class Tetris:
    def __init__(self):
        self.mixer = Mixer()
        self.renderer = Renderer()

        self.running = True

    def initialize(self):
        pygame.init()
        self.mixer.initialize()
        self.renderer.initialize()

    def quit(self):
        pygame.quit()

    def run(self):
        self.initialize()

        fps_clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            fps_clock.tick(120)

        self.quit()
