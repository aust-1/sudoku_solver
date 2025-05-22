"""BaseConstraint module.
This module defines the BaseConstraint class, which serves as a base for all Sudoku constraints.
It provides methods to check if the constraint is satisfied on a given grid and to auto-complete the grid based on the constraint.
The BaseConstraint class is not intended to be instantiated directly. Instead, it should be subclassed to create specific constraints.
Raises:
    NotImplementedError: Method not implemented.
    NotImplementedError: Method not implemented.
"""

from common import Grid


class BaseConstraint:
    """A class representing a base constraint for the Sudoku board."""

    def __init__(self):
        """Initialize the base constraint."""

    def check(self, grid: Grid) -> bool:
        """Check if the constraint is satisfied on the given grid.

        Args:
            grid (Grid): The Sudoku grid to check.

        Returns:
            bool: True if the constraint is satisfied, False otherwise.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def auto_complete(self, grid: Grid) -> bool:
        """Auto-complete the grid based on the constraint.

        Args:
            grid (Grid): The Sudoku grid to auto-complete.

        Returns:
            bool: True if the auto-completion was successful, False otherwise.
        """
        raise NotImplementedError("Subclasses should implement this method.")

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
        return set()
