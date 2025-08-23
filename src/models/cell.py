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
        self._row = row
        self._col = col
        self._value: int | None = None
        self._candidates: set[int] = set(range(1, size + 1))
        self._reachable_cells: set[Cell] = set()
        self._clone_cells: set[Cell] = {self}
        self._logger = Logger(
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
                self._reachable_cells |= cell.clone_cells

    def add_clones(self, cells: Iterable[Cell]) -> None:
        """Add clone cells to this cell's set.

        Args:
            cells (Iterable[Cell]): The cells to add.

        """
        for cell in cells:
            self._clone_cells |= cell.clone_cells

    def is_filled(self) -> bool:
        """Check if the cell is filled.

        Returns:
            bool: ``True`` if the cell has a value, ``False`` otherwise.

        """
        return self._value is not None

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, v: int | None) -> None:
        """Set the value of the cell.

        Args:
            v (int | None): The value to set.

        """
        self._logger.info(f"Set value {v}")
        self._value = v
        if v is None:
            return
        self._candidates.clear()
        self._candidates.add(v)
        for cell in self._reachable_cells:
            cell.eliminate_candidate(v)

    @property
    def candidates(self) -> set[int]:
        return self._candidates

    @candidates.setter
    def candidates(self, c: set[int]) -> None:
        """Set the candidates of the cell.

        Args:
            c (set[int]): The candidates to set.

        """
        self._candidates = c
        self._logger.info(f"Set candidates {c}")

    @property
    def reachable_cells(self) -> set[Cell]:
        return self._reachable_cells

    @property
    def clone_cells(self) -> set[Cell]:
        return self._reachable_cells

    def eliminate_candidate(self, v: int) -> bool:
        """Remove a value from the candidate set.

        Args:
            v (int): The value to remove.

        Returns:
            bool:
            ``True`` if the value was removed, ``False`` if it was not a candidate.

        """
        if v not in self._candidates:
            return False
        self._candidates.remove(v)
        self._logger.info(f"Eliminated candidate {v}")
        if len(self._candidates) == 1:
            self.value = next(iter(self._candidates))
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
        return (self._row, self._col) == (value.row, value.col)

    @override
    def __hash__(self) -> int:
        """Return a hash of the cell.

        Returns:
            int: The hash of the cell.

        """
        return hash((self._row, self._col))

    @override
    def __str__(self) -> str:
        """Return a string representation of the cell.

        Returns:
            str: A string representation of the cell.

        """
        return str(self._value) if self._value is not None else "."

    @override
    def __repr__(self) -> str:
        """Return a string representation of the cell.

        Returns:
            str: A string representation of the cell.

        """
        return f"C{self._row}.{self._col}"


# TODO: row and col en +1
