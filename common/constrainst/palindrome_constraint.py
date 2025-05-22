"""
Palindrome Constraint Module.
This module defines the PalindromeConstraint class, which applies constraints to palindrome Sudoku pieces.
"""

from common import BaseConstraint, Grid, CloneConstraint


class PalindromeConstraint(BaseConstraint):
    """A class representing a palindrome constraint for Sudoku pieces."""

    def __init__(self, palindrome_pieces: list[(int, int)]):
        """Initialize the palindrome constraint with a list of coordinates.

        Args:
            palindrome_pieces (list[(int, int)]): The list of coordinates to apply constraints to.
        """
        super().__init__()
        self.palindrome = palindrome_pieces
        self.clone_constraints = []
        for i in range(len(palindrome_pieces) // 2):
            self.clone_constraints.append(
                CloneConstraint({palindrome_pieces[i], palindrome_pieces[-(i + 1)]})
            )

    def check(self, grid: Grid) -> bool:
        """Check if the palindrome constraint is satisfied.

        Args:
            grid (Grid): The Sudoku grid to check.

        Returns:
            bool: True if the constraint is satisfied, False otherwise.
        """
        for constraint in self.clone_constraints:
            if not constraint.check(grid):
                return False
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Automatically complete the palindrome constraint.

        Args:
            grid (Grid): The Sudoku grid to complete.

        Returns:
            bool: True if the grid was successfully completed, False otherwise.
        """
        for constraint in self.clone_constraints:
            if not constraint.auto_complete(grid):
                return False
        return True
