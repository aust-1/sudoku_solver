from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board


class BacktrackingSolver(Solver):
    """Recursive backtracking solver used as a last resort."""

    def apply(self, board: Board) -> bool:
        """Attempt to solve the Sudoku board using backtracking.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if the board is solved, `False` otherwise.
        """
        if not board.is_valid():
            return False
        if board.is_solved():
            return True

        unfilled = [cell for cell in board.get_all_cells() if not cell.is_filled()]
        unfilled.sort(key=lambda c: len(c.candidates))
        cell = unfilled[0]

        for cand in list(cell.candidates):
            self.logger.debug(
                f"Trying {cand} at ({cell.row}, {cell.col}) in backtracking",
            )
            copy = board.deep_copy()
            copy.get_cell(cell.row, cell.col).set_value(cand)
            solver = BacktrackingSolver()
            if solver.apply(copy):
                board.copy_values_from(copy)
                self.logger.info(
                    f"Backtracking succeeded with {cand} at ({cell.row}, {cell.col})",
                )
                return True
        self.logger.info(f"Backtracking failed for cell ({cell.row}, {cell.col})")
        return False
