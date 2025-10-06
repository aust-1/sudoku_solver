from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload, override

from loggerplusplus import Logger

from models import Cell
from solver.constraints.factory import create_constraint_from_dict

if TYPE_CHECKING:
    from collections.abc import Iterable

    from solver.constraints.base_constraint import BaseConstraint


class Board:
    """Represents the Sudoku board as a 9x9 grid of :class:``Cell`` objects."""

    def __init__(self, size: int) -> None:
        """Initialize the Sudoku board.

        Args:
            size (int): The size of the Sudoku board (e.g., 9 for a 9x9 board).
        """
        self._size = size
        self._grid: list[list[Cell]] = [
            [Cell(r, c, self._size) for c in range(self._size)]
            for r in range(self._size)
        ]
        self._constraints: set[BaseConstraint] = set()
        self._regions: dict[str, set[Cell]] = {}
        self._logger = Logger(identifier="Board", follow_logger_manager_rules=True)
        self._init_regions()
        self._init_reachability()

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any]) -> Board:
        """Load the board from a dictionary representation.

        Args:
            input_dict (dict[str, Any]):
                The dictionary representation of the board.

        Returns:
            Board: The loaded Sudoku board.
        """
        board = cls(input_dict["size"])
        board._load_cells_from_dict(input_dict["cells"])
        board._load_constraint_from_dict(input_dict["constraint"])
        return board

    def to_dict(self) -> dict[str, Any]:
        """Convert the board to a dictionary representation.

        Returns:
            dict[str, Any]: The dictionary representation of the board.
        """
        return {
            "size": self._size,
            "cells": {cell.pos: [cell.candidates] for cell in self.get_all_cells()},
            "constraint": [c.to_dict() for c in self._constraints],
        }

    def _init_reachability(self) -> None:
        """Initialise reachable cells for each cell."""
        for cell in self.get_all_cells():
            cell.reachable_cells.clear()

        for region in self._regions.values():
            for cell in region:
                cell.add_reachables(region)

        for constraint in self._constraints:
            for cell in self.get_all_cells():
                cell.add_reachables(constraint.reachable_cells(self, cell))
        for constraint in self._constraints:
            for cell in self.get_all_cells():
                cell.add_reachables(constraint.reachable_cells(self, cell))
        # TODO: add_reachables => bool (modify or not), add while

    def _init_regions(self) -> None:
        """Initialise the regions of the board."""
        for i in range(self._size):
            self._regions[f"row{i}"] = self._get_row(i)
            self._regions[f"col{i}"] = self._get_col(i)
            self._regions[f"box{i}"] = self._get_box(i)

        for constraint in self._constraints:
            self._regions |= constraint.get_regions(self)
        # TODO: create a constraint, is not always classic regions

    def _get_row(self, r: int) -> set[Cell]:
        """Return all cells in row ``r``.

        Args:
            r (int): The row index of the cells.

        Returns:
            set[Cell]: All cells in the specified row.
        """
        return set(self._grid[r])

    def _get_col(self, c: int) -> set[Cell]:
        """Return all cells in column ``c``.

        Args:
            c (int): The column index of the cells.

        Returns:
            set[Cell]: All cells in the specified column.
        """
        return {self._grid[r][c] for r in range(self._size)}

    def _get_box(self, box_index: int) -> set[Cell]:
        """Return all cells in box ``box_index`` (0..8).

        Args:
            box_index (int): The index of the box (0..8).

        Returns:
            set[Cell]: All cells in the specified box.
        """
        start_r = (box_index // 3) * 3
        start_c = (box_index % 3) * 3
        return {
            self._grid[r][c]
            for r in range(start_r, start_r + 3)
            for c in range(start_c, start_c + 3)
        }

    @property
    def size(self) -> int:
        return self._size

    @property
    def constraints(self) -> set[BaseConstraint]:
        return self._constraints

    @property
    def regions(self) -> dict[str, set[Cell]]:
        return self._regions

    def add_constraints(self, *constraints: BaseConstraint) -> None:
        """Add constraints to the board and update reachability.

        Args:
            *constraints (BaseConstraint): The constraints to add.
        """
        for c in constraints:
            self._logger.debug(f"Adding constraint {c.__class__.__name__}")
            self._constraints.add(c)
            self._regions |= c.get_regions(self)
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))

        for c in constraints:
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))
        # TODO: idem refact with while

        for c in constraints:
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))

    @overload
    def get_cell(self, *, row: int, col: int) -> Cell: ...
    @overload
    def get_cell(self, *, pos: str) -> Cell: ...

    def get_cell(
        self,
        *,
        row: int | None = None,
        col: int | None = None,
        pos: str | None = None,
    ) -> Cell:
        """Return the cell at the specified row, column, or position.

        Args:
            row (int | None): The row index of the cell.
            col (int | None): The column index of the cell.
            pos (str | None): Position formatted like ``a2`` for row 1, column 2.

        Returns:
            Cell: The cell at the specified row and column or position.

        Raises:
            ValueError: If no argument is provided or the format is invalid.
        """
        if pos is not None:
            if (
                len(pos) != 2
                or not ord("a") <= ord(pos[0]) < ord("a") + self._size
                or not 1 <= int(pos[1]) <= self._size
            ):
                msg = f"Wrong position format: {pos}"
                self._logger.error(msg)
                raise ValueError(msg)
            return self._grid[ord(pos[0]) - ord("a")][int(pos[1]) - 1]
        if row is not None and col is not None:
            if not 0 <= row < self._size or not 0 <= col < self._size:
                msg = f"Wrong index format: r{row}c{col}"
                self._logger.error(msg)
                raise ValueError(msg)
            return self._grid[row][col]
        msg = "No argument provided"
        self._logger.error(msg)
        raise ValueError(msg)

    def get_all_cells(self) -> Iterable[Cell]:
        """Yield all cells in the board row by row.

        Yields:
            Cell: A cell in the board.
        """
        for row in self._grid:
            yield from row

    def is_valid(self) -> bool:
        """Check if the board is valid according to Sudoku rules.

        Returns:
            bool:
                ``True`` if all rows, columns and boxes contain no duplicates,
                ``False`` otherwise.
        """

        def region_valid(cells: Iterable[Cell]) -> bool:
            """Check if a region (row, column, box, ...) is valid.

            Args:
                cells (Iterable[Cell]): The cells in the region.

            Returns:
                bool: ``True`` if the region has no duplicates, ``False`` otherwise.

            """
            values = [c.value for c in cells if c.is_filled()]
            return len(values) == len(set(values))

        basic_valid = all(region_valid(r) for r in self._regions.values())
        if not basic_valid:
            self._logger.debug("Basic validity check failed")
            return False
        self._logger.debug("Basic validity check passed")
        return all(not constraint.check(self) for constraint in self._constraints)

    def is_solved(self) -> bool:
        """Check if the board is completely filled.

        Returns:
            bool: ``True`` if every cell has a value, ``False`` otherwise.
        """
        return (
            all(cell.is_filled() for cell in self.get_all_cells()) and self.is_valid()
        )

    def load_from_string(self, input_str: str) -> None:
        """Load digits into the board from a string (0 for empty).

        Args:
            input_str (str): A string representation of the Sudoku board.
        """
        self._logger.debug("Loading board from string")
        digits = [d for d in input_str if d.isdigit()]
        for idx, d in enumerate(digits[: self._size * self._size]):
            if d != "0":
                r, c = divmod(idx, self._size)
                self._grid[r][c].value = int(d)

    def _load_cells_from_dict(self, cells_dict: dict[str, list[int]]) -> None:
        """Load cell values from a dictionary representation.

        Args:
            cells_dict (dict[str, list[int]]):
                The dictionary representation of the cells.
        """
        for c, values in cells_dict.items():
            cell = self.get_cell(pos=c)
            cell.candidates = set(values)

    def _load_constraint_from_dict(
        self,
        constraint_dict: list[dict[str, Any]],
    ) -> None:
        """Load constraints from dictionary representation.

        Args:
            constraint_dict (list[dict[str, Any]]):
                List of dictionaries containing constraint configurations.
                Format: [{"type": "palindrome", "cells": ["a1", "a2", ...]}].

        Raises:
            ValueError: If constraint type is unknown or data is invalid.
        """
        self._logger.debug("Loading constraints from dict")
        for constraint_data in constraint_dict:
            try:
                constraint = create_constraint_from_dict(self, constraint_data)
                self.add_constraints(constraint)
                self._logger.info(f"Loaded constraint: {constraint}")
            except ValueError as e:
                self._logger.error(f"Failed to load constraint: {e}")
                raise

    # TODO: Load stylé fichier, interface ?

    @override
    def __str__(self) -> str:
        """Return a string representation of the board.

        Returns:
            str: A string representation of the Sudoku board.
        """
        lines: list[str] = []
        for r in range(self._size):
            row = " ".join(str(self._grid[r][c]) for c in range(self._size))
            lines.append(row)
        return "\n".join(lines)

    def deep_copy(self) -> Board:
        """Create a deep copy of the board.

        Returns:
            Board: A deep copy of the board.
        """
        board = Board(self._size)
        for r in range(self._size):
            for c in range(self._size):
                cell = self._grid[r][c]
                copy_cell = board._grid[r][c]
                copy_cell.value = cell.value
                copy_cell.candidates = set(cell.candidates)

        board._constraints = set()
        for constraint in self._constraints:
            board.add_constraints(constraint.deep_copy())
        return board

    def copy_values_from(self, other: Board) -> None:
        """Copy values and candidates from another board.

        Args:
            other (Board): The board to copy values from.
        """
        for r in range(self._size):
            for c in range(self._size):
                self._grid[r][c].value = other._grid[r][c].value
                self._grid[r][c].candidates = set(other._grid[r][c].candidates)
