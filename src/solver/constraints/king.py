from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell


class KingConstraint(BaseConstraint):
    """A class representing a king's movement constraint."""

    def __init__(self) -> None:
        """Initialize the king's movement constraint."""
        super().__init__(ConstraintType.KING)

    @override
    def check(self, board: Board) -> bool:
        """Check if the king's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: ``True`` if the king's movement is valid, ``False`` otherwise.

        """
        for i in range(board.size):
            for j in range(board.size):
                value = board.get_cell(i, j).value
                if value is not None:
                    neighbor_cells = self.reachable_cells(board, board.get_cell(i, j))
                    for cell in neighbor_cells:
                        if cell.value is not None and cell.value != value:
                            self.logger.debug(
                                f"King constraint violated at cell ({i}, {j})"
                                f" and neighbor cell ({cell.row}, {cell.col})"
                                f" with value {value}",
                            )
                            return False
        return True

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the king's movement constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.

        """
        return False

    @override
    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.

        """
        reachable: set[Cell] = set()
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (
                    0 <= cell.row + x < board.size
                    and 0 <= cell.col + y < board.size
                    and (x or y)
                ):
                    reachable.add(board.get_cell(cell.row + x, cell.col + y))
        return reachable

    @override
    def deep_copy(self) -> KingConstraint:
        """Create a deep copy of the constraint.

        Returns:
            KingConstraint: A deep copy of the constraint.

        """
        return KingConstraint()
