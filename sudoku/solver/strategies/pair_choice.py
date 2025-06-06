from __future__ import annotations

from collections import Counter

from sudoku.models import Board
from sudoku.solver.solver import Solver


class PairChoiceStrategy(Solver):
    """If a digit appears as candidate only once in a region, fill it."""

    def apply(self, board: Board) -> bool:
        """Fill cells with candidates that appear only once in their region.

        Args:
            board (Board): The Sudoku board to solve.

        Returns:
            bool: `True` if any cells were filled, `False` otherwise.
        """
        self.logger.info("PairChoiceStrategy running")
        moved = False
        regions = [
            [board.get_row(i) for i in range(9)],
            [board.get_col(i) for i in range(9)],
            [board.get_box(i) for i in range(9)],
        ]
        for region_group in regions:
            for region in region_group:
                counter = Counter(
                    cand
                    for cell in region
                    if not cell.is_filled()
                    for cand in cell.candidates
                )
                for cell in region:
                    if not cell.is_filled():
                        unique = [c for c in cell.candidates if counter[c] == 1]
                        if len(unique) == 1:
                            cell.set_value(unique[0])
                            moved = True
        return moved
