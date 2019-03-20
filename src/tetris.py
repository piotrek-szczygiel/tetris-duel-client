import pygame

from src.bag import Bag
from src.board import Board, BACKGROUND_RGB
from src.mixer import Mixer
from src.piece import Piece


class Tetris:
    def __init__(self):
        self.mixer = Mixer()

        self.bag = Bag()
        self.board = Board()

        self.display = None
        self.running = False

        self.current_piece = None

    def initialize(self):
        self.mixer.initialize()
        pygame.init()

        self.bag.initialize()
        self.board.initialize()

        self.display = pygame.display.set_mode((1500, 1000))
        pygame.display.set_caption("Tetris")

    def quit(self):
        pygame.quit()

    def render(self):
        self.display.fill(BACKGROUND_RGB)

        self.board.render()
        self.display.blit(self.board.surface, (0, 0))

    def update(self):
        pass

    def run(self):
        self.initialize()
        self.running = True

        self.current_piece = Piece(*self.bag.pop_tetromino())

        fps_clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                        (event.type == pygame.KEYDOWN
                         and event.key == pygame.K_q)):
                    self.running = False

            self.render()
            pygame.display.flip()

            fps_clock.tick(120)

        self.quit()
