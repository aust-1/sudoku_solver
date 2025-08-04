from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint
from sudoku.solver.constraints.killer import KillerConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell
    from sudoku.utils.gui import SudokuGUI


class XVConstraint(BaseConstraint):
    """A class representing a XV constraint."""

    def __init__(self, xv_cells: set[Cell], total_sum: int) -> None:
        """Initialize the XV constraint.

        Args:
            xv_cells (set[Cell]): The cells to constrain.
            total_sum (int): The sum to constrain the cells to.

        Raises:
            ValueError: If the cells are not adjacent.
            ValueError: If the sum is not a valid Sudoku value.
        """
        super().__init__()
        self.cell1, self.cell2 = xv_cells
        if (abs(self.cell1.row - self.cell2.row) == 1) == (
            abs(self.cell1.col - self.cell2.col) == 1
        ):
            msg = "XV constraint cells must be adjacent."
            raise ValueError(msg)
        self.killer_constraint: KillerConstraint = KillerConstraint(
            {self.cell1, self.cell2},
            total_sum=total_sum,
            board_size=9,
        )

    @classmethod
    def x(cls, x_cells: set[Cell]) -> XVConstraint:
        """Create a X constraint.

        Args:
            x_cells (set[Cell]): The cells to constrain.

        Returns:
            XVConstraint: The created XV constraint.
        """
        return cls(x_cells, total_sum=10)

    @classmethod
    def v(cls, v_cells: set[Cell]) -> XVConstraint:
        """Create a V constraint.

        Args:
            v_cells (set[Cell]): The cells to constrain.

        Returns:
            XVConstraint: The created XV constraint.
        """
        return cls(v_cells, total_sum=5)

    def check(self, board: Board) -> bool:
        """Check if the XV constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: `True` if the XV constraint is satisfied, `False` otherwise.
        """
        return self.killer_constraint.check(board)

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the XV constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        return self.killer_constraint.eliminate(board)

    def draw(self, gui: SudokuGUI) -> None:
        """Draw this XV constraint on `gui` if supported.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        gui.write_text_between_cells(
            self.cell1,
            self.cell2,
            "X" if self.killer_constraint.sum == 10 else "V",
        )
        # FIXME: c'est dégueulasse

    def deep_copy(self) -> XVConstraint:
        """Create a deep copy of the constraint.

        Returns:
            BaseConstraint: A deep copy of the constraint.
        """
        return XVConstraint(
            {self.cell1, self.cell2},
            total_sum=self.killer_constraint.sum,
        )


# QUESTION: init par set ou deux cells
