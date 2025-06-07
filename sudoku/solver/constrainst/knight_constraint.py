from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constrainst.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class KnightConstraint(BaseConstraint):
    """A class representing a knight's movement constraint."""

    def __init__(self) -> None:
        """Initialize the knight's movement constraint."""
        super().__init__()
        self.size = 9

    def check(self, board: Board) -> bool:
        """Check if the knight's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: ``True`` if the knight's movement is valid, ``False`` otherwise.
        """
        for i in range(self.size):
            for j in range(self.size):
                value = board.get_cell(i, j).value
                if value is not None:
                    reachable_cells = self.reachable_cells(board, board.get_cell(i, j))
                    for cell in reachable_cells:
                        neighbor_value = cell.value
                        if neighbor_value is not None and neighbor_value != value:
                            return False
        return True

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the knight's movement constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        eliminated = False
        for i in range(self.size):
            for j in range(self.size):
                value = board.get_cell(i, j).value
                if value is not None:
                    reachable_cells = self.reachable_cells(board, board.get_cell(i, j))
                    for cell in reachable_cells:
                        eliminated |= cell.eliminate(value)
        return eliminated

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
                    if 0 <= x < self.size and 0 <= y < self.size:
                        reachable.add(board.get_cell(x, y))
        return reachable
