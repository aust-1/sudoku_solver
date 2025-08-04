from __future__ import annotations

from typing import TYPE_CHECKING, override

from src.sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from src.sudoku.models import Board


class EliminationStrategy(Solver):
    """For each filled cell, remove its value from peers' candidates."""

    @override
    def apply(self, board: Board) -> bool:
        """Eliminate candidates using already placed values.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: ``True`` if any candidates were eliminated, ``False`` otherwise.

        """
        self.logger.debug("EliminationStrategy running")
        moved = False

        for name, region in board.regions.items():
            if len(region) != board.size:
                continue
            for digit in range(1, board.size + 1):
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

                eliminated = False
                for peer in reachable_cells:
                    eliminated |= peer.eliminate(digit)
                if eliminated:
                    moved = True
                    self.logger.debug(
                        f"Eliminated due to intersection of {cells} in {name}",
                    )

        return moved
