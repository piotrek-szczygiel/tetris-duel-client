import pygame
from blinker import signal

from brain import Brain
from mixer import Mixer
from renderer import Renderer


class Tetris:
    def __init__(self):
        self.mixer = Mixer()
        self.brain = Brain()
        self.renderer = Renderer()

        self.running = True

    def initialize(self):
        pygame.init()
        self.renderer.initialize_display()

    def quit(self):
        pygame.quit()

    def run(self):
        self.initialize()

        self.brain.new_piece()
        fps_clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                        (event.type == pygame.KEYDOWN
                         and event.key == pygame.K_q)):
                    self.running = False

            self.brain.tick()
            self.renderer.tick(self.brain)
            fps_clock.tick(120)

        signal('cleanup').send()
        self.quit()
