from __future__ import annotations

from sudoku.models import Board

from ..solver import Solver


class ConstraintStrategy(Solver):
    """Apply additional constraints to eliminate candidates."""

    def apply(self, board: Board) -> bool:
        moved = False
        for constraint in board.constraints:
            moved |= constraint.eliminate(board)
        return moved
