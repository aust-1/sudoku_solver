from __future__ import annotations

from itertools import combinations
from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board


class XWingStrategy(Solver):
    """Eliminate candidates using the X-Wing technique."""

    def apply(self, board: Board) -> bool:
        """Apply the X-Wing strategy to the board.

        Args:
            board: The Sudoku board.

        Returns:
            ``True`` if any candidates were eliminated, ``False`` otherwise.
        """
        self.logger.info("XWingStrategy running")
        moved = False
        digits = range(1, board.size + 1)

        for digit in digits:
            row_candidates: dict[int, tuple[int, int]] = {}
            for r in range(board.size):
                cols = [
                    c
                    for c in range(board.size)
                    if (
                        not board.get_cell(r, c).is_filled()
                        and digit in board.get_cell(r, c).candidates
                    )
                ]
                if len(cols) == 2:
                    row_candidates[r] = (cols[0], cols[1])
            for r1, r2 in combinations(row_candidates, 2):
                if row_candidates[r1] == row_candidates[r2]:
                    c1, c2 = row_candidates[r1]
                    for r in range(board.size):
                        if r in {r1, r2}:
                            continue
                        for c in (c1, c2):
                            cell = board.get_cell(r, c)
                            if cell.eliminate(digit):
                                moved = True

        for digit in digits:
            col_candidates: dict[int, tuple[int, int]] = {}
            for c in range(board.size):
                rows = [
                    r
                    for r in range(board.size)
                    if (
                        not board.get_cell(r, c).is_filled()
                        and digit in board.get_cell(r, c).candidates
                    )
                ]
                if len(rows) == 2:
                    col_candidates[c] = (rows[0], rows[1])
            for c1, c2 in combinations(col_candidates, 2):
                if col_candidates[c1] == col_candidates[c2]:
                    r1, r2 = col_candidates[c1]
                    for c in range(board.size):
                        if c in {c1, c2}:
                            continue
                        for r in (r1, r2):
                            cell = board.get_cell(r, c)
                            if cell.eliminate(digit):
                                moved = True

        return moved
