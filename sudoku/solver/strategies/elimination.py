from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board


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
            val = cell.value
            if val is not None:
                for peer in cell.reachable_cells:
                    moved |= peer.eliminate(val)
        regions = (
            [board.get_row(i) for i in range(9)]
            + [board.get_col(i) for i in range(9)]
            + [board.get_box(i) for i in range(9)]
        )
        # FIXME: c'est pas les seules régions, diagonales, extrabox, bishop, etc. refact avec contraintes
        for region in regions:
            for digit in range(1, 10):
                cells = [
                    cell
                    for cell in region
                    if not cell.is_filled() and digit in cell.candidates
                ]
                if len(cells) == 0:
                    continue
                reachable_cells = set(board.get_all_cells())
                for cell in cells:
                    reachable_cells.intersection_update(cell.reachable_cells)
                for peer in reachable_cells:
                    moved |= peer.eliminate(digit)
        return moved
