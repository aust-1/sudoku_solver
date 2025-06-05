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
        moved = False
        for r in range(9):
            for c in range(9):
                cell = board.get_cell(r, c)
                if cell.is_filled():
                    val = cell.value
                    peers = set(
                        board.get_row(r)
                        + board.get_col(c)
                        + board.get_box(3 * (r // 3) + c // 3)
                    )
                    peers.discard(cell)
                    for peer in peers:
                        if val in peer.candidates:
                            peer.eliminate(val)
                            moved = True
        return moved
