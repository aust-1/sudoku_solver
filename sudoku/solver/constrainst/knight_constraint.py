from __future__ import annotations

from sudoku.models import Board, Cell

from .base_constraint import BaseConstraint


class KnightConstraint(BaseConstraint):
    """A class representing a knight's movement constraint."""

    def check(self, board: Board) -> bool:
        """Check if the knight's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: ``True`` if the knight's movement is valid, ``False`` otherwise.
        """
        for i in range(9):
            for j in range(9):
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
            bool: ``True`` if at least one candidate was eliminated, ``False`` otherwise.
        """
        eliminated = False
        for i in range(9):
            for j in range(9):
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
        reachable = set()
        knight_moves = [(2, 1), (1, 2)]
        sign = [-1, 1]
        for dx, dy in knight_moves:
            for sign_x in sign:
                for sign_y in sign:
                    x = cell.row + dx * sign_x
                    y = cell.col + dy * sign_y
                    if 0 <= x < 9 and 0 <= y < 9:
                        reachable.add(board.get_cell(x, y))
        return reachable
