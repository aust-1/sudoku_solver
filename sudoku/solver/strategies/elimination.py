from __future__ import annotations

from sudoku.models import Board, Cell

from ..solver import Solver


class EliminationStrategy(Solver):
    """For each filled cell, remove its value from peers' candidates."""

    def apply(self, board: Board) -> bool:
        """Eliminate candidates using already placed values.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if any candidates were eliminated, `False` otherwise.
        """
        self.logger.info("EliminationStrategy running")
        moved = False
        for cell in board.get_all_cells():
            if cell.is_filled():
                val = cell.value
                for peer in cell.reachable_cells:
                    if val in peer.candidates:
                        peer.eliminate(val)
                        moved = True
        return moved
