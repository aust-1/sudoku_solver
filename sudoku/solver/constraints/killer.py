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
        self.possible_combinations: set[frozenset[int]] = set()
        for combination in combinations(range(1, board_size + 1), len(cells)):
            if sum(combination) == total_sum:
                self.possible_combinations.add(frozenset(combination))

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the killer constraint is satisfied.

        Returns:
            bool: `True` if the killer constraint is satisfied, `False` otherwise.
        """
        return any(cell.value is None for cell in self.killer_cells) or (
            sum(cell.value for cell in self.killer_cells if cell.value is not None)
            == self.sum
        )

    def _eliminate_combinations(self) -> None:
        """Eliminate invalid combinations based on the current state of the board."""
        # Remove combinations that not contain filled cells
        for cell in self.killer_cells:
            if cell.is_filled():
                value = cell.value
                self.possible_combinations = {
                    comb for comb in self.possible_combinations if value in comb
                }

        valid_combinations: set[frozenset[int]] = set()
        for combination in self.possible_combinations:
            # Check that each digit appears in at least one candidate cell
            if not all(
                any(
                    (c.value == digit or digit in c.candidates)
                    for c in self.killer_cells
                )
                for digit in combination
            ):
                continue

            # Check that every cell can take at least one digit of the combination
            if any(
                not cell.is_filled()
                and not any(d in cell.candidates for d in combination)
                for cell in self.killer_cells
            ):
                continue

            valid_combinations.add(frozenset(combination))
        self.possible_combinations = valid_combinations

    def _eliminate_candidates(self) -> bool:
        """Eliminate candidates based on the current possible combinations.

        Returns:
            bool: `True` if any candidates were eliminated, `False` otherwise.
        """
        eliminated = False

        # Force a digit if only one cell can contain it
        digits = set(self.possible_combinations.pop())
        for comb in self.possible_combinations:
            digits.intersection_update(comb)

        for digit in digits:
            possible_cells = [
                cell
                for cell in self.killer_cells
                if (not cell.is_filled() and digit in cell.candidates)
                or cell.value == digit
            ]
            if len(possible_cells) == 1 and not possible_cells[0].is_filled():
                possible_cells[0].set_value(digit)
                eliminated = True

        # Eliminate candidates that are not in any remaining combination
        for cell in self.killer_cells:
            if cell.is_filled():
                continue
            allowed_digits = {
                d
                for comb in self.possible_combinations
                for d in comb
                if d in cell.candidates
            }
            for digit in set(cell.candidates):
                if digit not in allowed_digits:
                    eliminated |= cell.eliminate(digit)
        return eliminated

    def eliminate(self, board: Board) -> bool:  # noqa: ARG002
        """Automatically complete the killer constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        eliminated = False

        self._eliminate_combinations()

        if self.possible_combinations:
            eliminated |= self._eliminate_candidates()

        return eliminated
