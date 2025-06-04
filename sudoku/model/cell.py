from __future__ import annotations
"""Module containing the :class:`Cell` model."""

from typing import Set


class Cell:
    """Represents a cell in the Sudoku grid."""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.value: int | None = None
        self.candidates: Set[int] = set(range(1, 10))

    def is_filled(self) -> bool:
        return self.value is not None

    def set_value(self, v: int) -> None:
        self.value = v
        self.candidates.clear()

    def eliminate(self, v: int) -> None:
        self.candidates.discard(v)

    def __repr__(self) -> str:
        return str(self.value) if self.value is not None else "."
