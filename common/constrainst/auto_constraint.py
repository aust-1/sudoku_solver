"""
Auto Constraint Module.
This module defines the AutoConstraint class, which automatically applies constraints to Sudoku pieces.
"""

from common import BaseConstraint, Grid


class AutoConstraint(BaseConstraint):
    """A class representing an automatic constraint for Sudoku pieces."""

    def __init__(self):
        """Initialize the auto constraint with a list of pieces.

        Args:
            pieces (list[Piece]): The list of pieces to apply constraints to.
        """
        super().__init__()

    def check(self, grid: Grid) -> bool:
        """Check if the auto constraint can be applied to the pieces.
        Args:
            grid (Grid): The Sudoku grid.
        Returns:
            bool: True if the constraint can be applied, False otherwise.
        """
        for i in range(grid.get_size()):
            for j in range(grid.get_size()):
                if not grid.get_piece(i, j).get_possible_values()[
                    grid.get_piece(i, j).get_value() - 1
                ]:
                    return False
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Apply the auto constraint to the pieces.

        Args:
            grid (Grid): The Sudoku grid.
        Returns:
            bool: True if the auto-completion was successful, False otherwise.
        """
        for i in range(grid.get_size()):
            for j in range(grid.get_size()):
                if (
                    grid.get_piece(i, j).get_possible_values().count(True) == 1
                    and grid.get_piece(i, j).get_value() is None
                ):
                    grid.get_piece(i, j).set_value(
                        grid.get_piece(i, j).get_possible_values().index(True) + 1
                    )
        return True
