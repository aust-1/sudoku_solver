from __future__ import annotations

from typing import TYPE_CHECKING, override

from loggerplusplus import Logger

if TYPE_CHECKING:
    from collections.abc import Iterable


class Cell:
    """Represents a cell in the Sudoku grid."""

    def __init__(self, row: int, col: int, size: int) -> None:
        """Initialise an empty cell at ``row``, ``col``.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            size (int): The size of the Sudoku grid.

        """
        self.row = row
        self.col = col
        self.value: int | None = None
        self.candidates: set[int] = set(range(1, size + 1))
        self.reachable_cells: set[Cell] = set()
        self.clones: set[Cell] = {self}
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
                self.reachable_cells.update(cell.clones)

    def is_filled(self) -> bool:
        """Check if the cell is filled.

        Returns:
            bool: ``True`` if the cell has a value, ``False`` otherwise.

        """
        return self.value is not None

    def set_value(self, v: int) -> None:
        """Set the value of the cell.

        Args:
            v (int): The value to set.

        """
        self.value = v
        self.candidates.clear()
        self.candidates.add(v)
        self.logger.info(f"Set value {v}")
        for cell in self.reachable_cells:
            cell.eliminate(v)

    def eliminate(self, v: int) -> bool:
        """Remove a value from the candidate set.

        Args:
            v (int): The value to remove.

        Returns:
            bool:
            ``True`` if the value was removed, ``False`` if it was not a candidate.

        """
        if v not in self.candidates:
            return False
        self.candidates.remove(v)
        self.logger.info(f"Eliminated candidate {v}")
        if len(self.candidates) == 1:
            self.set_value(next(iter(self.candidates)))
            return True
        return True

    @override
    def __eq__(self, value: object) -> bool:
        """Check if this cell is equal to another cell.

        Args:
            value (object): The object to compare.

        Returns:
            bool: ``True`` if the objects are equal, ``False`` otherwise.
        """
        if not isinstance(value, Cell):
            return False
        return (self.row, self.col) == (value.row, value.col)

    @override
    def __hash__(self) -> int:
        """Return a hash of the cell.

        Returns:
            int: The hash of the cell.

        """
        return hash((self.row, self.col))

    @override
    def __str__(self) -> str:
        """Return a string representation of the cell.

        Returns:
            str: A string representation of the cell.

        """
        return str(self.value) if self.value is not None else "."

    @override
    def __repr__(self) -> str:
        """Return a string representation of the cell.

        Returns:
            str: A string representation of the cell.

        """
        return f"C{self.row}.{self.col}"


# TODO: row and col en +1
