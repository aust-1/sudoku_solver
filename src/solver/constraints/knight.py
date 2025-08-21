from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell


class KnightConstraint(BaseConstraint):
    """A class representing a knight's movement constraint."""

    def __init__(self) -> None:
        """Initialize the knight's movement constraint."""
        super().__init__(ConstraintType.KNIGHT)

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the knight's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            set[Cell]:
                A set of cells that do not satisfy the knight's movement constraint.

        """
        invalid_cells: set[Cell] = set()
        for i in range(board.size):
            for j in range(board.size):
                current_cell = board.get_cell(i, j)
                value = current_cell.value
                if value is not None:
                    reachable_cells = self.reachable_cells(board, current_cell)
                    for cell in reachable_cells:
                        neighbor_value = cell.value
                        if neighbor_value is not None and neighbor_value == value:
                            self.logger.debug(
                                f"Knight constraint violated at cell ({i}, {j})"
                                f" and neighbor cell ({cell.row}, {cell.col})"
                                f" with value {value}",
                            )
                            invalid_cells |= {current_cell, cell}
        return invalid_cells

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the knight's movement constraint on the given board.

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
        knight_moves = [(2, 1), (1, 2)]
        signs = [-1, 1]
        for dx, dy in knight_moves:
            for sign_x in signs:
                for sign_y in signs:
                    x = cell.row + dx * sign_x
                    y = cell.col + dy * sign_y
                    if 0 <= x < board.size and 0 <= y < board.size:
                        reachable.add(board.get_cell(x, y))
        return reachable

    @override
    def deep_copy(self) -> KnightConstraint:
        """Create a deep copy of the constraint.

        Returns:
            KnightConstraint: A deep copy of the constraint.

        """
        return KnightConstraint()
