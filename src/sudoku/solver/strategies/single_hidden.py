from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board


class HiddenSingleStrategy(Solver):
    """If a digit appears as a candidate only once in a region, fill it."""

    def apply(self, board: Board) -> bool:
        """Fill cells with candidates that appear only once in their region.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if any cells were filled, `False` otherwise.
        """
        self.logger.debug("HiddenSingleStrategy running")
        moved = False
        for name, region in board.regions.items():
            if len(region) != board.size:
                continue
            counter = Counter(cand for cell in region for cand in cell.candidates)
            for cell in region:
                if not cell.is_filled():
                    unique = [c for c in cell.candidates if counter[c] == 1]
                    if len(unique) == 1:
                        cell.set_value(unique[0])
                        moved = True
                        self.logger.debug(
                            f"Filled due to hidden single in {name}",
                        )
        return moved
