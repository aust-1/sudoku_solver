"""
King's movement constraint
This module defines the KingConstraint class, which applies constraints to king pieces in a Sudoku-like grid.
"""

from common import BaseConstraint, Grid


class KingConstraint(BaseConstraint):
    """A class representing a king's movement constraint."""

    def __init__(self):
        """Initialize the king constraint."""
        super().__init__()

    def check(self, grid: Grid) -> bool:
        """Check if the king's movement is valid.

        Args:
            grid (Grid): The Sudoku grid.

        Returns:
            bool: True if the king's movement is valid, False otherwise.
        """
        size = grid.get_size()
        for i in range(size):
            for j in range(size):
                value = grid.get_piece(i, j).get_value()
                if value is not None:
                    neighbor_pieces = self.reachable_pieces(grid, (i, j))
                    for pos in neighbor_pieces:
                        if (
                            grid.get_piece(pos).get_value() is not None
                            and grid.get_piece(pos).get_value() != value
                        ):
                            return False
        return True

    def auto_complete(self, grid: Grid) -> bool:
        """Automatically complete the king's movement.

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
                    neighbor_pieces = self.reachable_pieces(grid, (i, j))
                    for pos in neighbor_pieces:
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
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (
                    0 <= position[0] + x < size
                    and 0 <= position[1] + y < size
                    and (x != 0 or y != 0)
                ):
                    reachable.add((position[0] + x, position[1] + y))
        return reachable
