from matrix import Matrix
from movement import Movement
from piece import Piece


class TSpin:
    @staticmethod
    def detect(matrix: Matrix, piece: Piece) -> bool:
        if piece.shape.name != "T":
            return False

        if piece.last_movement != Movement.rotate:
            return False

        piece_grid = piece.get_grid()
        x = piece.x + piece_grid.x
        y = piece.y + piece_grid.y

        matrix_grid = matrix.get_grid()

        occupied = 0

        if matrix_grid[y][x] != 0:
            occupied += 1

        if matrix.width <= x + 2 or matrix_grid[y][x + 2] != 0:
            occupied += 1

        if matrix.height <= y + 2 or matrix_grid[y + 2][x] != 0:
            occupied += 1

        if (
            matrix.width <= y + 2
            or matrix.height <= x + 2
            or matrix_grid[y + 2][x + 2] != 0
        ):
            occupied += 1

        return occupied >= 3
