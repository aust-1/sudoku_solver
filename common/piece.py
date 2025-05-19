"""Piece module.
This module defines the Piece class, which represents a piece in the Sudoku grid.
"""


class Piece:
    """A class representing a piece in the Sudoku grid."""

    def __init__(self, size: int):
        """Initialize the piece with its possible values.

        Args:
            size (int): The size of the piece (1-9).
        """
        self._value = None
        self._possible_values = set(range(1, size + 1))

    def __str__(self) -> str:
        """Return a string representation of the piece."""
        return str(self._value) if self._value is not None else "."

    def get_value(self) -> int:
        """Get the value of the piece.

        Returns:
            int: The value of the piece.
        """
        return self._value

    def set_value(self, value: int) -> bool:
        """Set the value of the piece.

        Args:
            value (int): The value to set.

        Returns:
            bool: True if the value was set successfully, False otherwise.
        """
        if value in self._possible_values:
            self._value = value
            self._possible_values.clear()
            self._possible_values.add(value)
            return True
        return False

    def get_possible_values(self) -> set:
        """Get the possible values of the piece.

        Returns:
            set: The possible values of the piece.
        """
        return self._possible_values

    def remove_possible_value(self, value: int) -> bool:
        """Remove a possible value from the piece.

        Args:
            value (int): The value to remove.

        Returns:
            bool: True if the value was removed successfully, False otherwise.
        """
        if value in self._possible_values:
            self._possible_values.remove(value)
            return True
        return False
