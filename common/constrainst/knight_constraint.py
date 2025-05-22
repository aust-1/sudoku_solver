"""
Knight's movement constraint
This module defines the KnightConstraint class, which applies constraints to knight pieces in a Sudoku-like grid.
"""

from common import BaseConstraint, Grid


class KnightConstraint(BaseConstraint):
    """A class representing a knight's movement constraint."""

    def __init__(self):
        """Initialize the knight constraint."""
        super().__init__()

    def check(self, grid: Grid) -> bool:
        """Check if the knight's movement is valid.

        Args:
            grid (Grid): The Sudoku grid.

        Returns:
            bool: True if the knight's movement is valid, False otherwise.
        """
        size = grid.get_size()
        for i in range(size):
            for j in range(size):
                value = grid.get_piece(i, j).get_value()
                if value is not None:
                    reachable_pieces = self.reachable_pieces(grid, (i, j))
                    for pos in reachable_pieces:
                        neighbor_value = grid.get_piece(pos).get_value()
                        if neighbor_value is not None and neighbor_value != value:
                            return False
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Automatically complete the knight's movement.

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
                    reachable_pieces = self.reachable_pieces(grid, (i, j))
                    for pos in reachable_pieces:
                        grid.get_piece(pos).remove_possible_value(value)
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
        size = grid.get_size()
        knight_moves = [(2, 1), (1, 2)]
        sign = [-1, 1]
        for dx, dy in knight_moves:
            for sign_x in sign:
                for sign_y in sign:
                    x = position[0] + dx * sign_x
                    y = position[1] + dy * sign_y
                    if 0 <= x < size and 0 <= y < size:
                        reachable.add((x, y))
        return reachable
