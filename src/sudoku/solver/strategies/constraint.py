from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board


class ConstraintStrategy(Solver):
    """Apply additional constraints to eliminate candidates."""

    def apply(self, board: Board) -> bool:  # noqa: PLR6301
        """Apply constraint strategies to the board.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if any candidates were eliminated, `False` otherwise.

        """
        moved = False
        for constraint in board.constraints:
            moved |= constraint.eliminate(board)
        return moved
