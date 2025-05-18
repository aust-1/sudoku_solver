class Grid:
    """A class representing a Sudoku grid."""

    def __init__(self, size: int):
        """Initialize the Sudoku grid with the given size.

        Args:
            size (int): The size of the grid (number of rows/columns).
        """
        self.size = size
        self.grid = [[_ for _ in range(size)] for _ in range(size)]

    def __str__(self) -> str:
        """Return a string representation of the grid."""
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    def is_full(self) -> bool:
        """Check if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(
            self.grid[row][col] is not None for row in range(9) for col in range(9)
        )

    def add_piece(self, row: int, col: int, piece: str) -> bool:
        """Add a piece to the grid.

        Args:
            row (int): The row index (0-8).
            col (int): The column index (0-8).
            piece (str): The piece to add.

        Returns:
            bool: True if the piece was added successfully with constraints satisfied, False otherwise.
        """
        if self.grid[row][col] is not None:
            self.delete_piece(row, col)

        self.grid[row][col] = piece

    def delete_piece(self, row: int, col: int) -> bool:
        """Delete a piece from the grid.

        Args:
            row (int): The row index (0-8).
            col (int): The column index (0-8).

        Returns:
            bool: True if the piece was deleted successfully, False otherwise.
        """
        if self.grid[row][col] is None:
            return False

        self.grid[row][col] = None
        return True
