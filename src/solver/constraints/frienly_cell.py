from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class FriendlyCellConstraint(BaseConstraint):
    """A class representing a friendly cell constraint."""

    def __init__(self, cell: Cell) -> None:
        """Initialize the friendly cell constraint.

        Args:
            cell (Cell): The cell to constrain.
        """
        super().__init__(ConstraintType.FRIENDLY_CELL)
        self.friendly_cell = cell

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> FriendlyCellConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "friendly_cell", "cell": "a1"}

        Returns:
            FriendlyCellConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cell" not in data:
            msg = "Friendly cell constraint requires 'cell' field"
            raise ValueError(msg)

        cell = board.get_cell(pos=data["cell"])
        return cls(cell)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "cell": self.friendly_cell.pos,
        }

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the friendly cell constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            set[Cell]:
                A set of cells that do not satisfy the friendly cell constraint.
        """
        if self.friendly_cell.value is not None and self.friendly_cell.value not in {
            self.friendly_cell.row + 1,
            self.friendly_cell.col + 1,
            self.friendly_cell.box + 1,
        }:
            return {self.friendly_cell}
        return set()

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the friendly cell constraint on the given board.

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
            if digit in {
                self.friendly_cell.row + 1,
                self.friendly_cell.col + 1,
                self.friendly_cell.box + 1,
            }:
                continue
            eliminated |= self.friendly_cell.eliminate_candidate(digit)
        if eliminated:
            self._logger.debug(
                "Eliminated due to friendly cell constraint",
            )
        return eliminated

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this friendly cell constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        # TODO: implement drawing (hearth)

    @override
    def deep_copy(self) -> FriendlyCellConstraint:
        """Create a deep copy of the constraint.

        Returns:
            FriendlyCellConstraint: A deep copy of the constraint.
        """
        return FriendlyCellConstraint(self.friendly_cell)

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        return f"FriendlyCellConstraint({self.friendly_cell})"
