import pygame


class Mixer:
    def __init__(self):
        pass

    def initialize(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
