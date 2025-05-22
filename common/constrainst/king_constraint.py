"""
King's movement constraint
This module defines the KingConstraint class, which applies constraints to king pieces in a Sudoku-like grid.
"""

from common import BaseConstraint, Grid


class KingConstraint(BaseConstraint):
    """A class representing a king's movement constraint."""

    def __init__(self):
        """Initialize the king constraint."""
        super().__init__()

    def check(self, grid: Grid) -> bool:
        """Check if the king's movement is valid.

        Args:
            grid (Grid): The Sudoku grid.

        Returns:
            bool: True if the king's movement is valid, False otherwise.
        """
        size = grid.get_size()
        for i in range(size):
            for j in range(size):
                value = grid.get_piece(i, j).get_value()
                if value is not None:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if (
                                0 <= i + x < size
                                and 0 <= j + y < size
                                and (x != 0 or y != 0)
                                and grid.get_piece(i + x, j + y).get_value() is not None
                                and grid.get_piece(i + x, j + y).get_value() != value
                            ):
                                return False
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Automatically complete the king's movement.

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
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if (
                                0 <= i + x < size
                                and 0 <= j + y < size
                                and (x != 0 or y != 0)
                            ):
                                grid.get_piece(i + x, j + y).remove_possible_value(
                                    value
                                )
        return True
