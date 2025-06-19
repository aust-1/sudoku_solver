from __future__ import annotations

import colorsys
from itertools import combinations
from typing import TYPE_CHECKING, ClassVar

from loggerplusplus import Logger  # type: ignore[import-untyped]

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell
    from sudoku.utils.gui import SudokuGUI


class KillerConstraint(BaseConstraint):
    """A class representing a killer constraint."""

    _killer_cage_index: ClassVar[int] = 0

    @classmethod
    def _next_killer_color(cls) -> tuple[int, int, int, int]:
        """Get the next color for a killer cage.

        Returns:
            tuple[int, int, int, int]: The RGBA color for the next killer cage.
        """
        hue = (cls._killer_cage_index * 0.15) % 1.0
        cls._killer_cage_index += 1
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255), 255)

    def __init__(self, cells: set[Cell], total_sum: int, board_size: int) -> None:
        """Initialize the killer constraint.

        Args:
            cells (set[Cell]): The cells to constrain.
            total_sum (int): The sum of the cell values.
            board_size (int): The size of the board.
        """
        super().__init__(
            Logger(
                identifier=f"{total_sum},{self.__class__.__name__}",
                follow_logger_manager_rules=True,
            ),
        )
        self.killer_cells = cells
        self.sum = total_sum
        self.possible_combinations: set[frozenset[int]] = set()
        self.color = self._next_killer_color()
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
                self.possible_combinations = {
                    comb for comb in self.possible_combinations if cell.value in comb
                }

        valid_combinations: set[frozenset[int]] = set()
        for comb in self.possible_combinations:
            # Check that each digit appears in at least one candidate cell
            if not all(
                any(
                    (c.value == digit or digit in c.candidates)
                    for c in self.killer_cells
                )
                for digit in comb
            ):
                self.logger.warning(
                    f"Invalid comb: {comb}, not all digits present in candidates",
                )
                continue

            # Check that every cell can take at least one digit of the combination
            if any(
                not cell.is_filled() and not any(d in cell.candidates for d in comb)
                for cell in self.killer_cells
            ):
                self.logger.debug(
                    f"Invalid comb: {comb}, not all cells can take a digit",
                )
                continue

            valid_combinations.add(frozenset(comb))
        self.possible_combinations = valid_combinations

    def _eliminate_candidates(self, board: Board) -> bool:
        """Eliminate candidates based on the current possible combinations.

        Args:
            board (Board): The Sudoku board to check against.

        Returns:
            bool: `True` if any candidates were eliminated, `False` otherwise.
        """
        eliminated = False

        # Eliminate candidates des cells reachs par les cellules qui ont une valeur qui
        # est dans l'intersection de toutes les combinaisons possibles
        # TODO: translate this comment
        digits = set(range(1, board.size + 1))
        for comb in self.possible_combinations:
            digits.intersection_update(comb)

        for digit in digits:
            possible_cells = [
                cell
                for cell in self.killer_cells
                if (not cell.is_filled() and digit in cell.candidates)
                or cell.value == digit
            ]

            reachable_cells: set[Cell] = set(board.get_all_cells())
            for cell in possible_cells:
                reachable_cells.intersection_update(cell.reachable_cells)
            reachable_cells.difference_update(possible_cells)

            for cell in reachable_cells:
                eliminated |= cell.eliminate(digit)

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

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the killer constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        self.logger.debug(
            f"Eliminating candidates for {self.__class__.__name__} constraint",
        )
        eliminated = False

        self._eliminate_combinations()

        if self.possible_combinations:
            eliminated |= self._eliminate_candidates(board)

        return eliminated

    def get_regions(self, board: Board) -> list[set[Cell]]:  # noqa: ARG002
        """Get the regions defined by the killer constraint.

        Args:
            board (Board): The Sudoku board.

        Returns:
            list[set[Cell]]: A list of sets of cells representing the regions.
        """
        return [self.killer_cells]

    def draw(self, gui: SudokuGUI) -> None:
        """Draw this bishop constraint on `gui` if supported.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        gui.draw_killer_cage(self.killer_cells, self.sum, self.color)


# TODO: centralisation des killer constraints pour faire toutes les sous cages
