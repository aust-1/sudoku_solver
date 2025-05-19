"""SelfExcludeConstraint module.
This module defines the SelfExcludeConstraint class, which is a specific type of constraint for Sudoku puzzles.
The SelfExcludeConstraint class inherits from the BaseConstraint class and implements methods to check if the constraint is satisfied on a given grid and to auto-complete the grid based on the constraint.
"""

from common import BaseConstraint, Grid, Piece


class SelfExcludeConstraint(BaseConstraint):
    """Constraint that excludes certain cells from being filled."""

    def __init__(self, excluded_cells: list[(int, int)]):
        super().__init__()
        self.excluded = set(excluded_cells)

    def check(self, grid: Grid) -> bool:
        """Check if the constraint is satisfied on the given grid.

        Args:
            grid (Grid): The Sudoku grid to check.

        Returns:
            bool: True if the constraint is satisfied, False otherwise.
        """
        values: set[int] = set()
        for row, col in self.excluded:
            if grid.get_piece(row, col) is not None:
                if grid.get_piece(row, col) in values:
                    return False
                values.add(grid.get_piece(row, col))
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Auto-complete the grid based on the constraint.

        Args:
            grid (Grid): The Sudoku grid to auto-complete.

        Returns:
            bool: True if the auto-completion was successful, False otherwise.
        """
        for row, col in self.excluded:
            if grid.get_piece(row, col).get_value() is not None:
                for row2, col2 in self.excluded:
                    if (row, col) != (row2, col2):
                        grid.get_piece(row2, col2).remove_possible_value(
                            grid.get_piece(row, col).get_value()
                        )
        return True
