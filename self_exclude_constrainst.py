"""SelfExcludeConstraint module.
This module defines the SelfExcludeConstraint class, which is a specific type of constraint for Sudoku puzzles.
The SelfExcludeConstraint class inherits from the BaseConstraint class and implements methods to check if the constraint is satisfied on a given grid and to auto-complete the grid based on the constraint.
"""

from base_constraint import BaseConstraint


class SelfExcludeConstraint(BaseConstraint):
    """Constraint that excludes certain cells from being filled."""

    def __init__(self, excluded_cells: list[(int, int)]):
        super().__init__()
        self.excluded = set(excluded_cells)

    def check(self, grid) -> bool:
        """Check if the constraint is satisfied on the given grid.

        Args:
            grid (Grid): The Sudoku grid to check.

        Returns:
            bool: True if the constraint is satisfied, False otherwise.
        """
        for row, col in self.excluded:
            if grid.grid[row][col] is not None:
                return False
        return True

    def auto_complete(self, grid) -> bool:
        """Auto-complete the grid based on the constraint.

        Args:
            grid (Grid): The Sudoku grid to auto-complete.

        Returns:
            bool: True if the auto-completion was successful, False otherwise.
        """
        for row, col in self.excluded:
            if grid.grid[row][col] is None:
                grid.grid[row][col] = "X"
        return True
