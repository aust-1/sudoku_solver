from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class GreaterThanConstraint(BaseConstraint):
    """A class representing a Greater Than constraint."""

    def __init__(self, higher_value_cell: Cell, lower_value_cell: Cell) -> None:
        """Initialize the Greater Than constraint.

        Args:
            higher_value_cell (Cell): The cells to constrain with the higher value.
            lower_value_cell (Cell): The cells to constrain with the lower value.

        Raises:
            ValueError:
                If the cells are not adjacent.
        """
        super().__init__(ConstraintType.GREATER_THAN)
        self.higher_value_cell, self.lower_value_cell = (
            higher_value_cell,
            lower_value_cell,
        )

        if (self.higher_value_cell.row - self.lower_value_cell.row) ** 2 + (
            self.higher_value_cell.col - self.lower_value_cell.col
        ) ** 2 != 1:
            msg = "Greater Than constraint cells must be adjacent."
            raise ValueError(msg)

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the Greater Than constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            set[Cell]: A set of cells that do not satisfy the Greater Than constraint.
        """
        if (
            self.higher_value_cell.value is not None
            and self.lower_value_cell.value is not None
            and not self.higher_value_cell.value > self.lower_value_cell.value
        ):
            return {self.higher_value_cell, self.lower_value_cell}
        return set()

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the Greater Than constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        eliminated = False

        cell1_candidates: set[int] = set(self.higher_value_cell.candidates)
        cell2_candidates: set[int] = set(self.lower_value_cell.candidates)
        max_c1 = max(cell1_candidates)
        min_c2 = min(cell2_candidates)

        for v1 in cell1_candidates:
            if v1 <= min_c2:
                eliminated |= self.higher_value_cell.eliminate_candidate(v1)

        for v2 in cell2_candidates:
            if v2 >= max_c1:
                eliminated |= self.lower_value_cell.eliminate_candidate(v2)

        if eliminated:
            self._logger.debug(
                f"Eliminated due to greater than in {self.higher_value_cell} > {self.lower_value_cell}",
            )
        return eliminated

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this Greater Than constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        # TODO: implement

    @override
    def deep_copy(self) -> GreaterThanConstraint:
        """Create a deep copy of the constraint.

        Returns:
            GreaterThanConstraint: A deep copy of the constraint.
        """
        return GreaterThanConstraint(
            self.higher_value_cell,
            self.lower_value_cell,
        )


# TODO: logic for greater than in series
