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
        self._possible_values = [True for _ in range(size)]

    def __str__(self) -> str:
        """Return a string representation of the piece."""
        return str(self._value) if self._value is not None else "."

    def get_value(self) -> int | None:
        """Get the value of the piece.

        Returns:
            int: The value of the piece.
        """
        return self._value

    def set_value(self, value: int | None) -> bool:
        """Set the value of the piece.

        Args:
            value (int | None): The value to set. ``None`` clears the piece.

        Returns:
            bool: True if the value was set successfully, False otherwise.
        """
        if value is None:
            self._value = None
            self._possible_values = [True for _ in range(len(self._possible_values))]
            return True

        if (
            1 <= value <= len(self._possible_values)
            and self._possible_values[value - 1]
        ):
            self._value = value
            self._possible_values = [False for _ in range(len(self._possible_values))]
            self._possible_values[value - 1] = True
            return True
        return False

    def get_possible_values(self) -> list[bool]:
        """Get the possible values of the piece.

        Returns:
            list[bool]: The possible values of the piece.
        """
        return self._possible_values

    def set_possible_values(self, possible_values: list[bool]) -> bool:
        """Set the possible values of the piece.

        Args:
            possible_values (list[bool]): The possible values to set.

        Returns:
            bool: True if the possible values were set successfully, False otherwise.
        """
        if len(possible_values) == len(self._possible_values):
            self._possible_values = possible_values
            return True
        return False

    def remove_possible_value(self, value: int) -> bool:
        """Remove a possible value from the piece.

        Args:
            value (int): The value to remove.

        Returns:
            bool: True if the value was removed successfully, False otherwise.
        """
        if 1 <= value <= len(self._possible_values):
            self._possible_values[value - 1] = False
            return True
        return False
