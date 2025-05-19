"""Grid module for Sudoku game.
This module defines the Grid class, which represents the Sudoku grid.
"""

from common import Piece


class Grid:
    """A class representing a Sudoku grid."""

    def __init__(self, size: int):
        """Initialize the Sudoku grid with the given size.

        Args:
            size (int): The size of the grid (number of rows/columns).
        """
        self._size = size
        self._grid = [[Piece(size) for _ in range(size)] for _ in range(size)]

    def __str__(self) -> str:
        """Return a string representation of the grid."""
        return "\n".join(" ".join(str(cell) for cell in row) for row in self._grid)

    def is_full(self) -> bool:
        """Check if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(
            self.get_piece(row, col) is not None
            for row in range(self._size)
            for col in range(self._size)
        )

    def get_piece(self, row: int, col: int) -> Piece:
        """Get the piece at the specified position.

        Args:
            row (int): The row index (0-8).
            col (int): The column index (0-8).

        Returns:
            int: The piece at the specified position, or None if empty.
        """
        return self._grid[row][col]

    def get_size(self) -> int:
        """Get the size of the grid.

        Returns:
            int: The size of the grid.
        """
        return self._size

    def add_piece(self, row: int, col: int, piece: int) -> bool:
        """Add a piece to the grid.

        Args:
            row (int): The row index (0-8).
            col (int): The column index (0-8).
            piece (int): The piece to add.

        Returns:
            bool: True if the piece was added successfully with constraints satisfied, False otherwise.
        """
        if self._grid[row][col] is not None:
            self.delete_piece(row, col)

        self._grid[row][col].set_value(piece)
        return True

    def delete_piece(self, row: int, col: int) -> bool:
        """Delete a piece from the grid.

        Args:
            row (int): The row index (0-8).
            col (int): The column index (0-8).

        Returns:
            bool: True if the piece was deleted successfully, False otherwise.
        """
        if self._grid[row][col] is None:
            return False

        self._grid[row][col].set_value(None)
        return True
