"""Board module for Sudoku game.
This module defines the Board class, which represents the Sudoku board.
"""

from common import Grid
from common import BaseConstraint, SelfExcludeConstraint


class Board:
    """A class representing the Sudoku board."""

    def __init__(self, size: int = 9):
        self._grid: Grid = Grid(size)
        self._constraints: list[BaseConstraint] = []
        self._constraints.append(SelfExcludeConstraint([(0, i) for i in range(size)]))
        self._constraints.append(SelfExcludeConstraint([(i, 0) for i in range(size)]))

    def __str__(self):
        """Return a string representation of the board."""
        return str(self._grid)

    def is_full(self) -> bool:
        """Check if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return self._grid.is_full()

    def add_piece(self, row: int, col: int, piece: int) -> bool:
        """Add a piece to the board.

        Args:
            row (int): The row index (0-8).
            col (int): The column index (0-8).
            piece (int): The piece to add.

        Returns:
            bool: True if the piece was added successfully with constraints satisfied, False otherwise.
        """
        self._grid.add_piece(row, col, piece)
        return self.check_constraints()

    def delete_piece(self, row: int, col: int) -> bool:
        """Delete a piece from the board.

        Args:
            row (int): The row index (0-8).
            col (int): The column index (0-8).

        Returns:
            bool: True if the piece was deleted successfully, False otherwise.
        """
        return self._grid.delete_piece(row, col)

    def check_constraints(self) -> bool:
        """Check if all constraints are satisfied.

        Returns:
            bool: True if all constraints are satisfied, False otherwise.
        """
        for constraint in self._constraints:
            if not constraint.check(self._grid):
                return False
        return True

    def add_constraint(self, constraint: BaseConstraint):
        """Add a constraint to the board.

        Args:
            constraint (BaseConstraint): The constraint to add.
        """
        self._constraints.append(constraint)

    def remove_constraint(self, constraint: BaseConstraint):
        """Remove a constraint from the board.

        Args:
            constraint (BaseConstraint): The constraint to remove.
        """
        self._constraints.remove(constraint)
