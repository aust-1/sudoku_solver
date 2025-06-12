from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class KingConstraint(BaseConstraint):
    """A class representing a king's movement constraint."""

    def check(self, board: Board) -> bool:
        """Check if the king's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: `True` if the king's movement is valid, `False` otherwise.
        """
        for i in range(board.size):
            for j in range(board.size):
                value = board.get_cell(i, j).value
                if value is not None:
                    neighbor_cells = self.reachable_cells(board, board.get_cell(i, j))
                    for cell in neighbor_cells:
                        if cell.value is not None and cell.value != value:
                            return False
        return True

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the king's movement constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        eliminated = False
        for i in range(board.size):
            for j in range(board.size):
                value = board.get_cell(i, j).value
                if value is not None:
                    neighbor_cells = self.reachable_cells(board, board.get_cell(i, j))
                    for cell in neighbor_cells:
                        eliminated |= cell.eliminate(value)
        return eliminated

    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:  # noqa: PLR6301
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
                    and (x != 0 or y != 0)
                ):
                    reachable.add(board.get_cell(cell.row + x, cell.col + y))
        return reachable
