"""Module defining the AxiaConstraint class, which represents a constraint based on the Axia Sudoku variant."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from models.cell import Cell
from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class AxiaConstraint(BaseConstraint):
    """A class representing an Axia Sudoku constraint."""

    def __init__(self, axia_cell: Cell) -> None:
        """Initialize the Axia constraint.

        Args:
            axia_cell (Cell): The cell that the Axia constraint applies to.
        """
        super().__init__(ConstraintType.AXIA)
        self.axia_cell = axia_cell

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> AxiaConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "axia", "cell": "a1"}

        Returns:
            AxiaConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cell" not in data:
            msg = "Axia constraint requires 'cell' field"
            raise ValueError(msg)

        position: str = data["cell"]
        cell: Cell = board.get_cell(pos=position)

        return cls(cell)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "cell": self.axia_cell.pos,
        }

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the Axia constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            set[Cell]:
                A set of cells that do not satisfy the Axia constraint.
        """
        invalid_cells: set[Cell] = set()
        value = self.axia_cell.value
        if value is not None:
            reachable_cells: set[Cell] = self.reachable_cells(board, self.axia_cell)
            for cell in reachable_cells:
                if cell.value is not None and cell.value == value:
                    self._logger.debug(
                        f"Axia constraint violated at cell {self.axia_cell.pos}"
                        f" and reacheable cell ({cell.row}, {cell.col})"
                        f" with value {value}",
                    )
                    invalid_cells |= {self.axia_cell, cell}
        return invalid_cells

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the axia constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        return False

    def _get_axia_reachable_cells(self, board: Board) -> set[Cell]:
        """Get the cells that are reachable from the axia cell.

        Returns:
            set[Cell]: A set of cells that are reachable from the axia cell.
        """
        axia_reachable_cells = set()
        for i in range(board.size):
            for j in range(board.size):
                if i == self.axia_cell.row or j == self.axia_cell.col:
                    continue
                if abs(i - self.axia_cell.row) != abs(j - self.axia_cell.col):
                    continue
                axia_reachable_cells.add(board.get_cell(row=i, col=j))
        return axia_reachable_cells

    @override
    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        if cell == self.axia_cell:
            return self._get_axia_reachable_cells(board)
        if cell in self._get_axia_reachable_cells(board):
            return {self.axia_cell}
        return set()

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this axia constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        # TODO: Implement drawing logic for Axia constraint

    @override
    def deep_copy(self) -> AxiaConstraint:
        """Create a deep copy of the constraint.

        Returns:
            AxiaConstraint: A deep copy of the constraint.
        """
        return AxiaConstraint(self.axia_cell)

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        return f"AxiaConstraint({self.axia_cell.pos})"
