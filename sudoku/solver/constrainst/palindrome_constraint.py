from __future__ import annotations
from .base_constraint import BaseConstraint
from sudoku.models import Board, Cell
from sudoku.solver import CloneConstraint


class PalindromeConstraint(BaseConstraint):
    """A class representing a palindrome constraint for Sudoku cells."""

    def __init__(self, palindrome_cells: list[Cell]):
        """Initialize the palindrome constraint with a list of coordinates.

        Args:
            palindrome_cells (list[Cell]): The list of cells to apply constraints to.
        """
        self.palindrome = palindrome_cells
        self.clone_constraints = []
        for i in range(len(palindrome_cells) // 2):
            self.clone_constraints.append(
                CloneConstraint({palindrome_cells[i], palindrome_cells[-(i + 1)]})
            )

    def check(self, board: Board) -> bool:
        """Check if the palindrome constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            bool: ``True`` if the constraint is satisfied, ``False`` otherwise.
        """
        for constraint in self.clone_constraints:
            if not constraint.check(board):
                return False
        return True

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the palindrome constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool: ``True`` if at least one candidate was eliminated, ``False`` otherwise.
        """
        eliminated = False
        for constraint in self.clone_constraints:
            eliminated |= constraint.eliminate(board)
        return eliminated

    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        reachable_cells = set()
        for constraint in self.clone_constraints:
            reachable_cells.update(constraint.reachable_cells(board, cell))
        return reachable_cells
