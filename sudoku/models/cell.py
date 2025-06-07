from __future__ import annotations

from typing import TYPE_CHECKING

from loggerplusplus import Logger

if TYPE_CHECKING:
    from collections.abc import Iterable


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
        self.candidates: set[int] = set(range(1, 10))
        self.reachable_cells: set[Cell] = set()
        self.logger = Logger(
            identifier=f"Cell {row}, {col}",
            follow_logger_manager_rules=True,
        )

    def add_reachables(self, cells: Iterable[Cell]) -> None:
        """Add reachable cells to this cell's set.

        Args:
            cells (Iterable[Cell]): The cells to add.
        """
        for cell in cells:
            if cell is not self:
                self.reachable_cells.add(cell)

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
        self.logger.info(f"Set value {v}")

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
        self.logger.info(f"Eliminated candidate {v}")
        return True

    def __repr__(self) -> str:
        """Return a string representation of the cell.

        Returns:
            str: A string representation of the cell.
        """
        return str(self.value) if self.value is not None else "."
