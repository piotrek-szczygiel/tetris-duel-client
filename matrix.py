import pygame


class Matrix:
    def __init__(self) -> None:
        self.width = 10
        self.height = 20
        self.vanish = 4

        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height + self.vanish)]

    def draw(self, display: pygame.display, x: int, y: int) -> None:
        pass
