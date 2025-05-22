"""
Knight's movement constraint
This module defines the KnightConstraint class, which applies constraints to knight pieces in a Sudoku-like grid.
"""

from common import BaseConstraint, Grid


class KnightConstraint(BaseConstraint):
    """A class representing a knight's movement constraint."""

    def __init__(self):
        """Initialize the knight constraint."""
        super().__init__()
        self.knight_moves = [(2, 1), (1, 2)]
        self.sign = [-1, 1]

    def check(self, grid: Grid) -> bool:
        """Check if the knight's movement is valid.

        Args:
            grid (Grid): The Sudoku grid.

        Returns:
            bool: True if the knight's movement is valid, False otherwise.
        """
        size = grid.get_size()
        for i in range(size):
            for j in range(size):
                value = grid.get_piece(i, j).get_value()
                if value is not None:
                    for dx, dy in self.knight_moves:
                        for sign_x in self.sign:
                            for sign_y in self.sign:
                                x = i + dx * sign_x
                                y = j + dy * sign_y
                                if 0 <= x < size and 0 <= y < size:
                                    neighbor_value = grid.get_piece(x, y).get_value()
                                    if (
                                        neighbor_value is not None
                                        and neighbor_value != value
                                    ):
                                        return False
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Automatically complete the knight's movement.

        Args:
            grid (Grid): The Sudoku grid.

        Returns:
            bool: True if the auto-completion was successful, False otherwise.
        """
        size = grid.get_size()
        for i in range(size):
            for j in range(size):
                value = grid.get_piece(i, j).get_value()
                if value is not None:
                    for dx, dy in self.knight_moves:
                        for sign_x in self.sign:
                            for sign_y in self.sign:
                                x = i + dx * sign_x
                                y = j + dy * sign_y
                                if 0 <= x < size and 0 <= y < size:
                                    grid.get_piece(x, y).remove_possible_value(value)
        return True
