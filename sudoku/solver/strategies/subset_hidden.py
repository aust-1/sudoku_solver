from __future__ import annotations

from itertools import combinations
from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class _BaseHiddenSubsetStrategy(Solver):
    """Base class for hidden subset strategies.

    Provides shared logic for hidden subsets of size N.
    """

    def __init__(self, size: int) -> None:
        """Initialise the base subset hidden strategy.

        Args:
            size (int): The size of the subset.
        """
        self.size = size
        super().__init__()

    @staticmethod
    def _eliminate_candidates(
        cells: set[Cell],
        combo: tuple[int, ...],
    ) -> bool:
        moved = False
        for cell in cells:
            for val in list(cell.candidates):
                if val not in combo:
                    moved |= cell.eliminate(val)
        return moved

    def apply(self, board: Board) -> bool:
        """Apply the hidden subset strategy.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: True if any candidates were eliminated, False otherwise.
        """
        self.logger.info(f"{self.__class__.__name__} running")
        moved = False
        digits: list[int] = list(range(1, board.size + 1))
        for region in board.regions:
            if len(region) != board.size:
                continue
            digit_cells: dict[int, set[Cell]] = {d: set() for d in digits}
            for cell in region:
                if cell.is_filled():
                    continue
                for d in cell.candidates:
                    digit_cells[d].add(cell)

            for combo in combinations(digits, self.size):
                cells_union: set[Cell] = set()
                for d in combo:
                    cells_union.update(digit_cells[d])
                if len(cells_union) != self.size:
                    continue
                if all(
                    digit_cells[d] <= cells_union
                    and 1 <= len(digit_cells[d]) <= self.size
                    for d in combo
                ):
                    moved |= self._eliminate_candidates(cells_union, combo)
        return moved


class HiddenPairStrategy(_BaseHiddenSubsetStrategy):
    """Hidden pair strategy.

    If a pair of specific digits appear as candidates in exactly two cells within a
    single region, remove other candidates from those cells.
    """

    def __init__(self) -> None:
        """Initialise the pair hidden strategy."""
        super().__init__(2)


class HiddenTripleStrategy(_BaseHiddenSubsetStrategy):
    """Hidden triple strategy.

    If a triplet of specific digits appear as candidates in exactly three cells within a
    single region, remove other candidates from those cells.
    """

    def __init__(self) -> None:
        """Initialise the triple hidden strategy."""
        super().__init__(3)


class HiddenQuadStrategy(_BaseHiddenSubsetStrategy):
    """Hidden quad strategy.

    If a quadruplet of specific digits appear as candidates in exactly four cells
    within a single region, remove other candidates from those cells.
    """

    def __init__(self) -> None:
        """Initialise the quad hidden strategy."""
        super().__init__(4)
