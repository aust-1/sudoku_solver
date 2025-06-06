from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterable, List, Set

from sudoku.models import Board, Cell
from sudoku.solver import Solver


class _BaseSubsetCandidateStrategy(Solver):
    """Base class for hidden subset strategies."""

    def __init__(self, size: int) -> None:
        """Initialise the base subset candidate strategy.

        Args:
            size (int): The size of the subset.
        """
        self.size = size
        super().__init__()

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

    def apply(self, board: Board) -> bool:
        """Apply the hidden subset candidate strategy.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: True if any candidates were eliminated, False otherwise.
        """
        self.logger.info(f"{self.__class__.__name__} running")
        moved = False
        digits: list[int] = list(range(1, 10))
        for region in self.regions(board):
            digit_cells: Dict[int, Set[Cell]] = {d: set() for d in digits}
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
                    for cell in cells_union:
                        for val in list(cell.candidates):
                            if val not in combo and cell.eliminate(val):
                                moved = True
        return moved


class PairCandidateStrategy(_BaseSubsetCandidateStrategy):
    """Pair candidate strategy for hidden subsets."""

    def __init__(self) -> None:
        super().__init__(2)


class TripleCandidateStrategy(_BaseSubsetCandidateStrategy):
    """Triple candidate strategy for hidden subsets."""

    def __init__(self) -> None:
        super().__init__(3)


class QuadCandidateStrategy(_BaseSubsetCandidateStrategy):
    """Quad candidate strategy for hidden subsets."""

    def __init__(self) -> None:
        super().__init__(4)
