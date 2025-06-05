from __future__ import annotations

from typing import Set


class Cell:
    """Represents a cell in the Sudoku grid."""

    def __init__(self, row: int, col: int) -> None:
        """Initialise an empty cell at ``row``, ``col``.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
        """
        self.row = row
        self.col = col
        self.value: int | None = None
        self.candidates: Set[int] = set(range(1, 10))

    def is_filled(self) -> bool:
        """Check if the cell is filled.

        Returns:
            bool: `True` if the cell has a value, `False` otherwise.
        """
        return self.value is not None

    def set_value(self, v: int) -> None:
        """Set the value of the cell.

        Args:
            v (int): The value to set.
        """
        self.value = v
        self.candidates.clear()

    def eliminate(self, v: int) -> bool:
        """Remove a value from the candidate set.

        Args:
            v (int): The value to remove.

        Returns:
            bool: `True` if the value was removed, `False` if it was not a candidate.
        """
        if v not in self.candidates:
            return False
        self.candidates.remove(v)
        return True

    def __repr__(self) -> str:
        """Return a string representation of the cell.

        Returns:
            str: A string representation of the cell.
        """
        return str(self.value) if self.value is not None else "."
