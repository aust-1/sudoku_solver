"""SelfExcludeConstraint module.
This module defines the SelfExcludeConstraint class, which is a specific type of constraint for Sudoku puzzles.
The SelfExcludeConstraint class inherits from the BaseConstraint class and implements methods to check if the constraint is satisfied on a given grid and to auto-complete the grid based on the constraint.
"""

from common import BaseConstraint, Grid


class SelfExcludeConstraint(BaseConstraint):
    """Constraint that excludes certain cells from being filled."""

    def __init__(self, excluded_pieces: list[tuple[int, int]]):
        """Initialize the self-exclude constraint.

        Args:
            excluded_cells (list[tuple[int, int]]): The list of excluded cells.
        """
        super().__init__()
        self.excluded = set(excluded_pieces)

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

    def reachable_pieces(
        self, grid: Grid, position: tuple[int, int]
    ) -> set[tuple[int, int]]:
        """Get the reachable pieces based on the constraint.

        Args:
            grid (Grid): The Sudoku grid.
            position (tuple[int, int]): The position of the piece.

        Returns:
            set[tuple[int, int]]: A set of reachable pieces.
        """
        reachable = set()
        for row, col in self.excluded:
            if (row, col) != position:
                reachable.add((row, col))
        return reachable
