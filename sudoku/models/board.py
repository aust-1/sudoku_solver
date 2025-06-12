from __future__ import annotations

from typing import TYPE_CHECKING

from loggerplusplus import Logger  # type: ignore[import-untyped]

from sudoku.models import Cell

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sudoku.solver.constraints.base_constraint import BaseConstraint

from sudoku.solver import (
    CloneConstraint,
    CloneZoneConstraint,
    KingConstraint,
    KnightConstraint,
    PalindromeConstraint,
)


class Board:
    """Represents the Sudoku board as a 9x9 grid of :class:`Cell` objects."""

    def __init__(self, size: int) -> None:
        """Initialize the Sudoku board.

        Args:
            size (int): The size of the Sudoku board (e.g., 9 for a 9x9 board).
        """
        self.size = size
        self.grid: list[list[Cell]] = [
            [Cell(r, c, self.size) for c in range(self.size)] for r in range(self.size)
        ]
        self.constraints: list[BaseConstraint] = []
        self.regions: list[set[Cell]] = []
        self.logger = Logger(identifier="Board", follow_logger_manager_rules=True)
        self._init_regions()
        self._init_reachability()

    def _init_reachability(self) -> None:
        """Initialise reachable cells for each cell."""
        for cell in self.get_all_cells():
            cell.reachable_cells.clear()

        for r in self.regions:
            for cell in r:
                cell.add_reachables(r)

        for constraint in self.constraints:
            for cell in self.get_all_cells():
                cell.add_reachables(constraint.reachable_cells(self, cell))
        for constraint in self.constraints:
            for cell in self.get_all_cells():
                cell.add_reachables(constraint.reachable_cells(self, cell))

    def _init_regions(self) -> None:
        """Initialise the regions of the board."""
        self.regions = (
            [self._get_row(r) for r in range(self.size)]
            + [self._get_col(c) for c in range(self.size)]
            + [self._get_box(b) for b in range(self.size)]
        )

        for constraint in self.constraints:
            self.regions.extend(constraint.get_regions())

    def _get_row(self, r: int) -> set[Cell]:
        """Return all cells in row `r`.

        Args:
            r (int): The row index of the cells.

        Returns:
            set[Cell]: All cells in the specified row.
        """
        return set(self.grid[r])

    def _get_col(self, c: int) -> set[Cell]:
        """Return all cells in column `c`.

        Args:
            c (int): The column index of the cells.

        Returns:
            set[Cell]: All cells in the specified column.
        """
        return {self.grid[r][c] for r in range(self.size)}

    def _get_box(self, box_index: int) -> set[Cell]:
        """Return all cells in box `box_index` (0..8).

        Args:
            box_index (int): The index of the box (0..8).

        Returns:
            set[Cell]: All cells in the specified box.
        """
        start_r = (box_index // 3) * 3
        start_c = (box_index % 3) * 3
        return {
            self.grid[r][c]
            for r in range(start_r, start_r + 3)
            for c in range(start_c, start_c + 3)
        }

    def add_constraints(self, *constraints: BaseConstraint) -> None:
        """Add constraints to the board and update reachability.

        Args:
            *constraints (BaseConstraint): The constraints to add.
        """
        for c in constraints:
            self.logger.info(f"Adding constraint {c.__class__.__name__}")
            self.constraints.append(c)
            self.regions.extend(c.get_regions())
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))
            for cell in self.get_all_cells():
                cell.add_reachables(c.reachable_cells(self, cell))

    def get_cell(self, row: int, col: int) -> Cell:
        """Return the cell at `row`, `col`.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            Cell: The cell at the specified row and column.
        """
        return self.grid[row][col]

    def get_all_cells(self) -> Iterable[Cell]:
        """Yield all cells in the board row by row.

        Yields:
            Iterator[Iterable[Cell]]:
                An iterator over the rows of the board,
                each yielding the cells in that row.
        """
        for row in self.grid:
            yield from row

    def is_valid(self) -> bool:
        """Check if the board is valid according to Sudoku rules.

        Returns:
            bool:
                `True` if all rows, columns and boxes contain no duplicates,
                `False` otherwise.
        """

        def region_valid(cells: Iterable[Cell]) -> bool:
            """Check if a region (row, column, box, ...) is valid.

            Args:
                cells (Iterable[Cell]): The cells in the region.

            Returns:
                bool: `True` if the region has no duplicates, `False` otherwise.
            """
            values = [c.value for c in cells if c.is_filled()]
            return len(values) == len(set(values))

        basic_valid = all(region_valid(r) for r in self.regions if len(r) == self.size)
        if not basic_valid:
            return False
        return all(constraint.check(self) for constraint in self.constraints)

    def is_solved(self) -> bool:
        """Check if the board is completely filled.

        Returns:
            bool: `True` if every cell has a value, `False` otherwise.
        """
        return (
            all(cell.is_filled() for cell in self.get_all_cells()) and self.is_valid()
        )

    def load_from(self, input_str: str) -> None:
        """Load digits into the board from a string (0 for empty).

        Args:
            input_str (str): A string representation of the Sudoku board.
        """
        self.logger.info("Loading board from string")
        digits = [d for d in input_str if d.isdigit()]
        for idx, d in enumerate(digits[: self.size * self.size]):
            if d != "0":
                r, c = divmod(idx, self.size)
                self.grid[r][c].set_value(int(d))

    # TODO: Load stylé fichier, interface ?

    def __str__(self) -> str:
        """Return a string representation of the board.

        Returns:
            str: A string representation of the Sudoku board.
        """
        lines: list[str] = []
        for r in range(self.size):
            row = " ".join(str(self.grid[r][c]) for c in range(self.size))
            lines.append(row)
        return "\n".join(lines)

    def deep_copy(self) -> Board:
        """Create a deep copy of the board.

        Returns:
            Board: A deep copy of the board.
        """
        board = Board(self.size)
        for r in range(self.size):
            for c in range(self.size):
                cell = self.grid[r][c]
                copy_cell = board.grid[r][c]
                copy_cell.value = cell.value
                copy_cell.candidates = set(cell.candidates)

        board.constraints = []
        for constraint in self.constraints:
            if isinstance(constraint, CloneConstraint):
                clone_cells = constraint.clone.copy()
                board.add_constraints(CloneConstraint(clone_cells))
            elif isinstance(constraint, CloneZoneConstraint):
                for clone_constraint in constraint.clone_constraints:
                    clone_cells = clone_constraint.clone.copy()
                    board.add_constraints(CloneConstraint(clone_cells))
            elif isinstance(constraint, PalindromeConstraint):
                palindrome_cells: list[Cell] = constraint.palindrome.copy()
                board.add_constraints(PalindromeConstraint(palindrome_cells))
            elif isinstance(constraint, KingConstraint):
                board.add_constraints(KingConstraint())
            elif isinstance(constraint, KnightConstraint):
                board.add_constraints(KnightConstraint())
        return board

    def copy_values_from(self, other: Board) -> None:
        """Copy values and candidates from another board.

        Args:
            other (Board): The board to copy values from.
        """
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c].value = other.grid[r][c].value
                self.grid[r][c].candidates = set(other.grid[r][c].candidates)
