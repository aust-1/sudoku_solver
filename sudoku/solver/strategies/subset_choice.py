from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class _BaseSubsetChoiceStrategy(Solver):
    """Base class for naked subset strategies."""

    def __init__(self, size: int) -> None:
        self.size = size
        super().__init__()

    def apply(self, board: Board) -> bool:
        """Apply the naked subset choice strategy.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: True if any candidates were eliminated, False otherwise.
        """
        self.logger.info(f"{self.__class__.__name__} running")
        moved = False
        for region in board.regions:
            groups: dict[frozenset[int], list[Cell]] = {}
            for cell in region:
                if not cell.is_filled() and len(cell.candidates) == self.size:
                    key = frozenset(cell.candidates)
                    groups.setdefault(key, []).append(cell)
            for cand_set, cells in groups.items():
                if len(cells) == self.size:
                    for cell in region:
                        if cell not in cells and not cell.is_filled():
                            for val in cand_set:
                                moved |= cell.eliminate(val)
        return moved


class PairChoiceStrategy(_BaseSubsetChoiceStrategy):
    """Pair choice strategy.

    If a pair of candidates appears only in two cells,
    eliminate them from other cells in the region.
    """

    def __init__(self) -> None:
        """Initialise the pair choice strategy."""
        super().__init__(2)


class TripleChoiceStrategy(_BaseSubsetChoiceStrategy):
    """Triple choice strategy.

    If a triplet of candidates appears only in three cells, eliminate them from other
    cells in the region.
    """

    def __init__(self) -> None:
        """Initialise the triple choice strategy."""
        super().__init__(3)


class QuadChoiceStrategy(_BaseSubsetChoiceStrategy):
    """Quad choice strategy.

    If a quadruplet of candidates appears only in four cells, eliminate them from other
    cells in the region.
    """

    def __init__(self) -> None:
        """Initialise the quad choice strategy."""
        super().__init__(4)
