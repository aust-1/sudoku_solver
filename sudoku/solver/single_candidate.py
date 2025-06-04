from __future__ import annotations

from sudoku.model.board import Board
from sudoku.model.cell import Cell

from .solver import Solver


class SingleCandidateStrategy(Solver):
    """Fill cells that have a single candidate."""

    def apply(self, board: Board) -> bool:
        """Fill cells that have a single candidate.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if any cells were filled, `False` otherwise.
        """
        moved = False
        for cell in board.get_all_cells():
            if not cell.is_filled() and len(cell.candidates) == 1:
                cell.set_value(next(iter(cell.candidates)))
                moved = True
        return moved
