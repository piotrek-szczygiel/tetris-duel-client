from typing import List

from popup import Popup
from text import Text


class Score:
    def __init__(self) -> None:
        self.score = 0
        self.combo = -1
        self.last_clear_was_hard = False
        self.lines = 0
        self.duel_lines = 0

    def update_clear(self, level: int, rows_cleared: List[int], t_spin: bool) -> Popup:
        rows = len(rows_cleared)
        lines = 0
        duel_lines = 0

        if rows == 1:
            if t_spin:
                duel_lines = 2
                if self.last_clear_was_hard:
                    lines = 12
                else:
                    lines = 8
            else:
                lines = 1
                duel_lines = 0
        elif rows == 2:
            if t_spin:
                duel_lines = 4
                if self.last_clear_was_hard:
                    lines = 18
                else:
                    lines = 12
            else:
                lines = 3
                duel_lines = 1
        elif rows == 3:
            if t_spin:
                duel_lines = 6
                if self.last_clear_was_hard:
                    lines = 24
                else:
                    lines = 16
            else:
                lines = 5
                duel_lines = 3
        elif rows == 4:
            if self.last_clear_was_hard:
                lines = 12
            else:
                lines = 8

            duel_lines = 4

        if self.last_clear_was_hard:
            duel_lines += 1

        self.score += lines * 100 * level
        self.lines = lines
        self.duel_lines = duel_lines

        color = "gold"

        if rows == 2:
            message = "Double"
        elif rows == 3:
            message = "Triple"
        elif rows == 4:
            message = "Tetris"
            color = "cyan"
        else:
            message = ""

        if t_spin:
            message += "\nT-Spin"
            color = "purple"

        if t_spin or rows == 4:
            if self.last_clear_was_hard:
                message += "\nBack-to-Back"
            else:
                self.last_clear_was_hard = True
        else:
            self.last_clear_was_hard = False

        self.combo += 1

        if self.combo > 0:
            self.score += 50 * self.combo * level

        return Popup(message, size=4, color=color, gcolor="white")

    def reset_combo(self) -> None:
        self.combo = -1

    def update_soft_drop(self, rows: int) -> None:
        self.score += rows

    def update_hard_drop(self, rows: int) -> None:
        self.score += 2 * rows

    def draw(self, x: int, y: int) -> None:
        Text().draw(str(self.score), (x, y + 30), gcolor="green")

        if self.combo > 0:
            Text().draw("Combo: " + str(self.combo), (x, y), gcolor="yellow")
