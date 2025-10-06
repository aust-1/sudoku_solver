from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.killer import KillerConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI

X_SUM = 10
V_SUM = 5


class XVConstraint(BaseConstraint):
    """A class representing a XV constraint."""

    def __init__(self, xv_cell1: Cell, xv_cell2: Cell, total_sum: int) -> None:
        """Initialize the XV constraint.

        Args:
            xv_cell1 (Cell): The first cell to constrain.
            xv_cell2 (Cell): The second cell to constrain.
            total_sum (int): The sum to constrain the cells to.

        Raises:
            ValueError:
                If the cells are not adjacent or if the sum is not a valid Sudoku value.
        """
        super().__init__(ConstraintType.X_V)
        self.cell1 = xv_cell1
        self.cell2 = xv_cell2

        if (self.cell1.row - self.cell2.row) ** 2 + (
            self.cell1.col - self.cell2.col
        ) ** 2 != 1:
            msg = "XV constraint cells must be adjacent."
            raise ValueError(msg)

        self.killer_constraint: KillerConstraint = KillerConstraint(
            {self.cell1, self.cell2},
            total_sum=total_sum,
            board_size=9,
        )

    @classmethod
    def x(
        cls,
        x_cell1: Cell,
        x_cell2: Cell,
    ) -> XVConstraint:
        """Create a X constraint.

        Args:
            x_cell1 (Cell): The first cell to constrain.
            x_cell2 (Cell): The second cell to constrain.

        Returns:
            XVConstraint: The created XV constraint.
        """
        return cls(x_cell1, x_cell2, total_sum=X_SUM)

    @classmethod
    def v(cls, v_cell1: Cell, v_cell2: Cell) -> XVConstraint:
        """Create a V constraint.

        Args:
            v_cell1 (Cell): The first cell to constrain.
            v_cell2 (Cell): The second cell to constrain.

        Returns:
            XVConstraint: The created XV constraint.
        """
        return cls(v_cell1, v_cell2, total_sum=V_SUM)

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> XVConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "xv", "cell1": "a1", "cell2": "a2", "sum": 10}

        Returns:
            XVConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cell1" not in data:
            msg = "XV constraint requires 'cell1' field"
            raise ValueError(msg)
        if "cell2" not in data:
            msg = "XV constraint requires 'cell2' field"
            raise ValueError(msg)
        if "sum" not in data:
            msg = "XV constraint requires 'sum' field"
            raise ValueError(msg)

        cell1 = board.get_cell(pos=data["cell1"])
        cell2 = board.get_cell(pos=data["cell2"])

        total_sum = int(data["sum"])

        return cls(cell1, cell2, total_sum)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "cell1": self.cell1.pos,
            "cell2": self.cell2.pos,
            "sum": self.killer_constraint.sum,
        }

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the XV constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            set[Cell]: A set of cells that do not satisfy the XV constraint.
        """
        return self.killer_constraint.check(board)

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the XV constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated, ``False`` otherwise.
        """
        return self.killer_constraint.eliminate(board)

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this XV constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        gui.write_text_between_cells(
            self.cell1,
            self.cell2,
            "X" if self.killer_constraint.sum == X_SUM else "V",
        )
        # FIXME: c'est dégueulasse

    @override
    def deep_copy(self) -> XVConstraint:
        """Create a deep copy of the constraint.

        Returns:
            XVConstraint: A deep copy of the constraint.
        """
        return XVConstraint(
            self.cell1,
            self.cell2,
            total_sum=self.killer_constraint.sum,
        )

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        xv_type = "X" if self.killer_constraint.sum == X_SUM else "V"
        return f"XVConstraint([{self.cell1.pos}, {self.cell2.pos}], {xv_type}={self.killer_constraint.sum})"


# QUESTION: init par set ou deux cells
