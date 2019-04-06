import pygame
from typing import List
Grid = List[List[int]]

class Board:
    def __init__(self, width=10, height=20) -> None:
        self.width: int = width
        self.height:int = height

        self.grid: Grid = [[0 for _ in range(width)] for _ in range(height)]
        self.piece: Piece

    def draw(self, display: pygame.display, x: int, y: int) -> None:
        pass
