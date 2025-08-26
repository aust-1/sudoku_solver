from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class GreaterThanConstraint(BaseConstraint):
    """A class representing a Greater Than constraint."""

    def __init__(self, cell: Cell, greater_than: Cell) -> None:
        """Initialize the Greater Than constraint.

        Args:
            cell (Cell): The cells to constrain with the higher value.
            greater_than (Cell): The cells to constrain with the lower value.

        Raises:
            ValueError:
                If the cells are not adjacent.

        """
        super().__init__(ConstraintType.GREATER_THAN)
        self.cell1, self.cell2 = cell, greater_than

        if (abs(self.cell1.row - self.cell2.row) == 1) == (
            abs(self.cell1.col - self.cell2.col) == 1
        ):
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
            self.cell1.value is not None
            and self.cell2.value is not None
            and not self.cell1.value > self.cell2.value
        ):
            return {self.cell1, self.cell2}
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

        cell1_candidates: set[int] = set(self.cell1.candidates)
        cell2_candidates: set[int] = set(self.cell2.candidates)
        max_c1 = max(cell1_candidates)
        min_c2 = min(cell2_candidates)

        for v1 in cell1_candidates:
            if v1 <= min_c2:
                eliminated |= self.cell1.eliminate_candidate(v1)

        for v2 in cell2_candidates:
            if v2 >= max_c1:
                eliminated |= self.cell2.eliminate_candidate(v2)

        if eliminated:
            self._logger.debug(
                f"Eliminated due to greater than in {self.cell1} > {self.cell2}",
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
            self.cell1,
            self.cell2,
        )


# TODO: logic for greater than in series
