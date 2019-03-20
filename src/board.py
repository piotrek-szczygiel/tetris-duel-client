class Board:
    def __init__(self):
        self.cols = 10
        self.rows = 20

        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
