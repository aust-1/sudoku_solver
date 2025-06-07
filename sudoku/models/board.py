from __future__ import annotations

from typing import TYPE_CHECKING

from loggerplusplus import Logger

from sudoku.models import Cell

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sudoku.solver.constrainst.base_constraint import BaseConstraint


class Board:
    """Represents the Sudoku board as a 9x9 grid of :class:`Cell` objects."""

    def __init__(self) -> None:
        """Create an empty board filled with cells."""
        self.grid: list[list[Cell]] = [[Cell(r, c) for c in range(9)] for r in range(9)]
        self.constraints: list[BaseConstraint] = []
        self.logger = Logger(identifier="Board", follow_logger_manager_rules=True)
        self._init_reachability()

    def _init_reachability(self) -> None:
        """Initialise reachable cells for each cell."""
        for cell in self.get_all_cells():
            cell.reachable_cells.clear()

        for r in range(9):
            row = self.get_row(r)
            for cell in row:
                cell.add_reachables(row)

        for c in range(9):
            col = self.get_col(c)
            for cell in col:
                cell.add_reachables(col)

        for b in range(9):
            box = self.get_box(b)
            for cell in box:
                cell.add_reachables(box)

        for constraint in self.constraints:
            for cell in self.get_all_cells():
                cell.add_reachables(constraint.reachable_cells(self, cell))

    def add_constraint(self, constraint: BaseConstraint) -> None:
        """Add a constraint to the board and update reachability.

        Args:
            constraint (BaseConstraint): The constraint to add.
        """
        self.logger.info(f"Adding constraint {constraint.__class__.__name__}")
        self.constraints.append(constraint)
        for cell in self.get_all_cells():
            cell.add_reachables(constraint.reachable_cells(self, cell))
        for cell in self.get_all_cells():
            cell.add_reachables(constraint.reachable_cells(self, cell))
        for cell in self.get_all_cells():
            cell.add_reachables(constraint.reachable_cells(self, cell))

    def get_cell(self, row: int, col: int) -> Cell:
        """Return the cell at ``row``, ``col``.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            Cell: The cell at the specified row and column.
        """
        return self.grid[row][col]

    def get_row(self, r: int) -> list[Cell]:
        """Return all cells in row ``r``.

        Args:
            r (int): The row index of the cells.

        Returns:
            List[Cell]: All cells in the specified row.
        """
        return list(self.grid[r])

    def get_col(self, c: int) -> list[Cell]:
        """Return all cells in column ``c``.

        Args:
            c (int): The column index of the cells.

        Returns:
            List[Cell]: All cells in the specified column.
        """
        return [self.grid[r][c] for r in range(9)]

    def get_box(self, box_index: int) -> list[Cell]:
        """Return all cells in box ``box_index`` (0..8).

        Args:
            box_index (int): The index of the box (0..8).

        Returns:
            List[Cell]: All cells in the specified box.
        """
        start_r = (box_index // 3) * 3
        start_c = (box_index % 3) * 3
        return [
            self.grid[r][c]
            for r in range(start_r, start_r + 3)
            for c in range(start_c, start_c + 3)
        ]

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
            """Check if a region (row, column, or box) is valid.

            Args:
                cells (Iterable[Cell]): The cells in the region.

            Returns:
                bool: `True` if the region has no duplicates, `False` otherwise.
            """
            values = [c.value for c in cells if c.is_filled()]
            return len(values) == len(set(values))

        basic_valid = all(
            region_valid(self.get_row(g))
            and region_valid(self.get_col(g))
            and region_valid(self.get_box(g))
            for g in range(9)
        )
        if not basic_valid:
            return False
        return all(constraint.check(self) for constraint in self.constraints)

    def is_solved(self) -> bool:
        """Check if the board is completely filled.

        Returns:
            bool: `True` if every cell has a value, `False` otherwise.
        """
        return all(cell.is_filled() for cell in self.get_all_cells())

    def load_from(self, input_str: str) -> None:
        """Load digits into the board from a string (0 for empty).

        Args:
            input_str (str): A string representation of the Sudoku board.
        """
        self.logger.info("Loading board from string")
        digits = [d for d in input_str if d.isdigit()]
        for idx, d in enumerate(digits[:81]):
            if d != "0":
                r, c = divmod(idx, 9)
                self.grid[r][c].set_value(int(d))

    # TODO: Load stylé fichier, interface ?

    def __str__(self) -> str:
        """Return a string representation of the board.

        Returns:
            str: A string representation of the Sudoku board.
        """
        lines: list[str] = []
        for r in range(9):
            row = " ".join(str(self.grid[r][c]) for c in range(9))
            lines.append(row)
        return "\n".join(lines)

    def deep_copy(self) -> Board:
        """Create a deep copy of the board.

        Returns:
            Board: A deep copy of the board.
        """
        board = Board()
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                copy_cell = board.grid[r][c]
                copy_cell.value = cell.value
                copy_cell.candidates = set(cell.candidates)

        from sudoku.solver import (
            CloneConstraint,
            CloneZoneConstraint,
            KingConstraint,
            KnightConstraint,
            PalindromeConstraint,
        )

        board.constraints = []
        for constraint in self.constraints:
            if isinstance(constraint, CloneConstraint):
                cells = {board.get_cell(c.row, c.col) for c in constraint.clone}
                board.add_constraint(CloneConstraint(cells))
            elif isinstance(constraint, CloneZoneConstraint):
                for clone_constraint in constraint.clone_constraints:
                    cells = {
                        board.get_cell(c.row, c.col) for c in clone_constraint.clone
                    }
                    board.add_constraint(CloneConstraint(cells))
            elif isinstance(constraint, PalindromeConstraint):
                cells = [board.get_cell(c.row, c.col) for c in constraint.palindrome]
                board.add_constraint(PalindromeConstraint(cells))
            elif isinstance(constraint, KingConstraint):
                board.add_constraint(KingConstraint())
            elif isinstance(constraint, KnightConstraint):
                board.add_constraint(KnightConstraint())
        return board

    def copy_values_from(self, other: Board) -> None:
        """Copy values and candidates from another board.

        Args:
            other (Board): The board to copy values from.
        """
        for r in range(9):
            for c in range(9):
                self.grid[r][c].value = other.grid[r][c].value
                self.grid[r][c].candidates = set(other.grid[r][c].candidates)
