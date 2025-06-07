from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board


class SingleCandidateStrategy(Solver):
    """Fill cells that have a single candidate."""

    def apply(self, board: Board) -> bool:
        """Fill cells that have a single candidate.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if any cells were filled, `False` otherwise.
        """
        self.logger.info("SingleCandidateStrategy running")
        moved = False
        for cell in board.get_all_cells():
            if not cell.is_filled() and len(cell.candidates) == 1:
                cell.set_value(cell.candidates.pop())
                moved = True
        return moved
