from __future__ import annotations

from itertools import combinations
from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class KillerConstraint(BaseConstraint):
    """A class representing a killer constraint."""

    def __init__(self, cells: set[Cell], total_sum: int, board_size: int) -> None:
        """Initialize the killer constraint.

        Args:
            cells (set[Cell]): The cells to constrain.
            total_sum (int): The sum of the cell values.
            board_size (int): The size of the board.
        """
        self.killer_cells = cells
        self.sum = total_sum
        self.possible_combinations: set[set[int]] = set()
        for combination in combinations(range(1, board_size + 1), len(cells)):
            if sum(combination) == total_sum:
                self.possible_combinations.add(set(combination))

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the killer constraint is satisfied.

        Returns:
            bool: `True` if the killer constraint is satisfied, `False` otherwise.
        """
        return any(cell.value is None for cell in self.killer_cells) or (
            sum(cell.value for cell in self.killer_cells if cell.value is not None)
            == self.sum
        )

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the killer constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        eliminated = False
        for cell in self.killer_cells:
            if cell.is_filled():
                for combination in self.possible_combinations:
                    if cell.value not in combination:
                        self.possible_combinations.remove(combination)
                        # FIXME: delete the combination in the set fix, copy ?
        # TODO: implement logic to obliger un nombre si le en fonction d'une région tel nombre est nécessairement dans la killer
        # TODO: implement logic to eliminate candidates based on the remaining possible combinations
        # TODO: implement logic to eliminate possible combinations that cannot be satisfied by the remaining cells
        return eliminated
