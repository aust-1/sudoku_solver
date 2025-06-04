from __future__ import annotations

from sudoku.model.board import Board
from sudoku.model.cell import Cell

from .solver import Solver


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
            copy = board.deep_copy()
            copy.get_cell(cell.row, cell.col).set_value(cand)
            solver = BacktrackingSolver()
            if solver.apply(copy):
                board.copy_values_from(copy)
                return True
        return False
