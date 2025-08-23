from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.solver import Solver

if TYPE_CHECKING:
    from models import Board, Cell


class _BaseNakedSubsetStrategy(Solver):
    """Base class for naked subset strategies.

    Provides shared logic for naked subsets of size N.
    """

    def __init__(self, size: int) -> None:
        """Initialise the base naked subset strategy.

        Args:
            size (int): The size of the subset.

        """
        self.size = size
        super().__init__()

    @staticmethod
    def _remove_candidates(
        region: set[Cell],
        cells: list[Cell],
        cand_set: frozenset[int],
    ) -> bool:
        moved = False
        for cell in region:
            if cell not in cells and not cell.is_filled():
                for val in cand_set:
                    moved |= cell.eliminate_candidate(val)
        return moved

    @override
    def apply(self, board: Board) -> bool:
        """Apply the naked subset choice strategy.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: True if any candidates were eliminated, False otherwise.

        """
        self._logger.debug(f"{self.__class__.__name__} running")
        moved = False
        for name, region in board.regions.items():
            groups: dict[frozenset[int], list[Cell]] = {}
            for cell in region:
                if not cell.is_filled() and len(cell.candidates) == self.size:
                    key = frozenset(cell.candidates)
                    groups.setdefault(key, []).append(cell)
            for cand_set, cells in groups.items():
                if len(cells) == self.size and self._remove_candidates(
                    region,
                    cells,
                    cand_set,
                ):
                    moved = True
                    self._logger.debug(
                        f"Eliminated due to naked subset {cand_set} in {name}",
                    )
        return moved


class NakedPairStrategy(_BaseNakedSubsetStrategy):
    """Naked pair strategy.

    If a pair of cells in the same region have only two identical digits as candidates,
    remove those candidates from other cells in the region.
    """

    def __init__(self) -> None:
        """Initialise the pair choice strategy."""
        super().__init__(2)


class NakedTripleStrategy(_BaseNakedSubsetStrategy):
    """Naked triple strategy.

    If a triplet of cells in the same region have only three identical digits as
    candidates, remove those candidates from other cells in the region.
    """

    def __init__(self) -> None:
        """Initialise the triple choice strategy."""
        super().__init__(3)


class NakedQuadStrategy(_BaseNakedSubsetStrategy):
    """Naked quad strategy.

    If a quadruplet of cells in the same region have only four identical digits as
    candidates, remove those candidates from other cells in the region.
    """

    def __init__(self) -> None:
        """Initialise the quad choice strategy."""
        super().__init__(4)
