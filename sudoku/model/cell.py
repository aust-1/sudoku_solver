from __future__ import annotations
"""Module containing the :class:`Cell` model."""

from typing import Set


class Cell:
    """Represents a cell in the Sudoku grid."""

    def __init__(self, row: int, col: int) -> None:
        """Initialise an empty cell at ``row``, ``col``."""
        self.row = row
        self.col = col
        self.value: int | None = None
        self.candidates: Set[int] = set(range(1, 10))

    def is_filled(self) -> bool:
        """Return ``True`` if the cell has a value."""
        return self.value is not None

    def set_value(self, v: int) -> None:
        """Assign ``v`` to the cell and clear candidates."""
        self.value = v
        self.candidates.clear()

    def eliminate(self, v: int) -> None:
        """Remove ``v`` from the candidate set."""
        self.candidates.discard(v)

    def __repr__(self) -> str:
        return str(self.value) if self.value is not None else "."
