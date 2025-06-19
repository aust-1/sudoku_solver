from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class UniversalConstraint(BaseConstraint):
    """A class representing a universal constraint."""

    def check(self, board: Board) -> bool:  # noqa: ARG002, PLR6301
        """Check if the universal constraint is satisfied.

        Returns:
            bool: `True` if the universal constraint is satisfied, `False` otherwise.
        """
        return True

    def eliminate(self, board: Board) -> bool:  # noqa: ARG002, PLR6301
        """Automatically complete the universal constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        return False

    def reachable_cells(  # noqa: PLR6301
        self,
        board: Board,
        cell: Cell,
    ) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        x = cell.row % 3
        y = cell.col % 3

        reachable_cells = {
            board.get_cell(i, j)
            for i in range(x, board.size, 3)
            for j in range(y, board.size, 3)
        }
        reachable_cells.discard(cell)

        return reachable_cells

    def get_regions(self, board: Board) -> list[set[Cell]]:  # noqa: PLR6301
        """Get the regions defined by the universal constraint.

        Args:
            board (Board): The Sudoku board.

        Returns:
            list[set[Cell]]: A list of sets of cells representing the regions.
        """
        regions: list[set[Cell]] = []

        for i in range(3):
            for j in range(3):
                region: set[Cell] = {
                    board.get_cell(x, y)
                    for x in range(i, board.size, 3)
                    for y in range(j, board.size, 3)
                }
                regions.append(region)

        return regions
