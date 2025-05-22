"""
Clone Constraint Module.
This module defines the CloneConstraint class, which applies constraints to cloned Sudoku pieces.
"""

from common import BaseConstraint, Grid


class CloneConstraint(BaseConstraint):
    """A class representing a clone constraint for Sudoku pieces."""

    def __init__(self, clone_pieces: set[(int, int)]):
        """Initialize the clone constraint with a list of coordinates.

        Args:
            clone_pieces (list[(int, int)]): The list of coordinates to apply constraints to.
        """
        super().__init__()
        self.clone = clone_pieces

    def check(self, grid: Grid) -> bool:
        """Check if the clone constraint is satisfied.

        Args:
            grid (Grid): The Sudoku grid to check.

        Returns:
            bool: True if the constraint is satisfied, False otherwise.
        """
        value = grid.get_piece(self.clone[0][0], self.clone[0][1]).get_value()
        for row, col in self.clone:
            if grid.get_piece(row, col).get_value() != value:
                return False
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Automatically complete the clone constraint.

        Args:
            grid (Grid): The Sudoku grid to complete.

        Returns:
            bool: True if the grid was successfully completed, False otherwise.
        """
        values: list[bool] = [True] * grid.get_size()
        for i in range(0, grid.get_size()):
            for coords in self.clone:
                values[i] &= grid.get_piece(coords).get_possible_values()[i]
        for coords in self.clone:
            grid.get_piece(coords).set_possible_values(values)
        return True
