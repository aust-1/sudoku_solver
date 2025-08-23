from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell


class UniversalConstraint(BaseConstraint):
    """A class representing a universal constraint."""

    def __init__(self) -> None:
        """Initialize the universal constraint."""
        super().__init__(ConstraintType.UNIVERSAL)

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the universal constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            set[Cell]: A set of cells that do not satisfy the universal constraint.

        """
        invalid_cells: set[Cell] = set()
        for i in range(board.size):
            for j in range(board.size):
                current_cell = board.get_cell(r=i, c=j)
                value = current_cell.value
                if value is not None:
                    neighbor_cells = self.reachable_cells(board, current_cell)
                    for cell in neighbor_cells:
                        if cell.value is not None and cell.value != value:
                            self._logger.debug(
                                f"Universal constraint violated at cell ({i}, {j})"
                                f" and cell ({cell.row}, {cell.col})"
                                f" with value {value}",
                            )
                            invalid_cells |= {current_cell, cell}
        return invalid_cells

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the universal constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.

        """
        return False

    @override
    def reachable_cells(
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
            board.get_cell(r=i, c=j)
            for i in range(x, board.size, 3)
            for j in range(y, board.size, 3)
        }
        reachable_cells.discard(cell)

        return reachable_cells

    @override
    def get_regions(self, board: Board) -> dict[str, set[Cell]]:
        """Get the regions defined by the universal constraint.

        Args:
            board (Board): The Sudoku board.

        Returns:
            dict[str,set[Cell]]: A dictionary of sets of cells representing the regions.

        """
        regions: dict[str, set[Cell]] = {}

        for i in range(3):
            for j in range(3):
                region: set[Cell] = {
                    board.get_cell(r=x, c=y)
                    for x in range(i, board.size, 3)
                    for y in range(j, board.size, 3)
                }
                regions[f"universal_{i}_{j}"] = region

        return regions

    @override
    def deep_copy(self) -> UniversalConstraint:
        """Create a deep copy of the constraint.

        Returns:
            UniversalConstraint: A deep copy of the constraint.

        """
        return UniversalConstraint()
