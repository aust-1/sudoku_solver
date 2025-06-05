from __future__ import annotations

from typing import Dict, Iterable, List

from sudoku.models import Board, Cell

from ..solver import Solver


class _BaseSubsetChoiceStrategy(Solver):
    """Base class for naked subset strategies."""

    def __init__(self, size: int) -> None:
        self.size = size

    def regions(self, board: Board) -> Iterable[List[Cell]]:
        """Get all regions (rows, columns, boxes) in the Sudoku board.

        Args:
            board (Board): The Sudoku board.

        Returns:
            Iterable[List[Cell]]: A list of all regions (rows, columns, boxes) in the Sudoku board.
        """
        # TODO: c'est pas les seules régions possibles, genre les diagonales, les régions personnalisées, les killers, etc.
        return (
            [board.get_row(i) for i in range(9)]
            + [board.get_col(i) for i in range(9)]
            + [board.get_box(i) for i in range(9)]
        )

    def apply(self, board: Board) -> bool:  # type: ignore[override]
        """Apply the naked subset choice strategy.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: True if any candidates were eliminated, False otherwise.
        """
        moved = False
        for region in self.regions(board):
            groups: Dict[frozenset[int], List[Cell]] = {}
            for cell in region:
                if not cell.is_filled() and len(cell.candidates) == self.size:
                    key = frozenset(cell.candidates)
                    groups.setdefault(key, []).append(cell)
            for cand_set, cells in groups.items():
                if len(cells) == self.size:
                    for cell in region:
                        if cell not in cells and not cell.is_filled():
                            for val in cand_set:
                                if val in cell.candidates:
                                    cell.eliminate(val)
                                    moved = True
        return moved


class PairChoiceStrategy(_BaseSubsetChoiceStrategy):
    """Pair choice strategy: If a pair of candidates appears only in two cells, eliminate them from other cells in the region."""

    def __init__(self) -> None:
        super().__init__(2)


class TripleChoiceStrategy(_BaseSubsetChoiceStrategy):
    """Triple choice strategy: If a triplet of candidates appears only in three cells, eliminate them from other cells in the region."""

    def __init__(self) -> None:
        super().__init__(3)


class QuadChoiceStrategy(_BaseSubsetChoiceStrategy):
    """Quad choice strategy: If a quadruplet of candidates appears only in four cells, eliminate them from other cells in the region."""

    def __init__(self) -> None:
        super().__init__(4)
