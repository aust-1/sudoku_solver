from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell
    from sudoku.utils.gui import SudokuGUI


class ParityConstraint(BaseConstraint):
    """A class representing a parity constraint."""

    def __init__(self, cell: Cell, rest: int) -> None:
        """Initialize the parity constraint.

        Args:
            cell (Cell): The cell to constrain.
            rest (int): The remainder when the cell value is divided by 2.

        """
        super().__init__()
        self.parity_cell = cell
        self.rest = rest

    @classmethod
    def even(cls, cell: Cell) -> ParityConstraint:
        """Create a parity constraint for even numbers.

        Args:
            cell (Cell): The cell to constrain.

        Returns:
            ParityConstraint: The created parity constraint.

        """
        return cls(cell, rest=0)

    @classmethod
    def odd(cls, cell: Cell) -> ParityConstraint:
        """Create a parity constraint for odd numbers.

        Args:
            cell (Cell): The cell to constrain.

        Returns:
            ParityConstraint: The created parity constraint.

        """
        return cls(cell, rest=1)

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the parity constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            bool: ``True`` if the parity constraint is satisfied, ``False`` otherwise.

        """
        return self.parity_cell.value is None or self.parity_cell.value % 2 == self.rest

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the parity constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.

        """
        eliminated = False
        digits = range(1, board.size + 1)

        for digit in digits:
            if digit % 2 == self.rest:
                continue
            eliminated |= self.parity_cell.eliminate(digit)
        if eliminated:
            self.logger.debug(
                "Eliminated due to parity constraint",
            )
        return eliminated

    def draw(self, gui: SudokuGUI) -> None:
        """Draw this bishop constraint on ``gui`` if supported.

        Args:
            gui (SudokuGUI): The GUI to draw on.

        """
        color = (200, 200, 200, 156)
        if self.rest == 1:
            gui.draw_circle_in_cell(self.parity_cell, color)
        else:
            gui.draw_square(self.parity_cell, color)

    def deep_copy(self) -> ParityConstraint:
        """Create a deep copy of the constraint.

        Returns:
            ParityConstraint: A deep copy of the constraint.

        """
        return ParityConstraint(self.parity_cell, self.rest)
