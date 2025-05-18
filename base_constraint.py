from grid import Grid


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
