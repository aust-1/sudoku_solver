from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class BishopConstraint(BaseConstraint):
    """A class representing a bishop's movement constraint."""

    def __init__(self, bishop_cells: set[Cell]) -> None:
        """Initialize the bishop's movement constraint."""
        super().__init__()
        self.bishop = bishop_cells

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the bishop's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: `True` if the bishop's movement is valid, `False` otherwise.
        """
        values: set[int] = set()
        for cell in self.bishop:
            if cell.value is not None:
                if cell.value in values:
                    return False
                values.add(cell.value)
        return True

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the bishop's movement constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        eliminated = False
        for cell in self.bishop:
            value = cell.value
            if value is not None:
                neighbor_cells = self.reachable_cells(board, cell)
                for neighbor_cell in neighbor_cells:
                    eliminated |= neighbor_cell.eliminate(value)
        return eliminated

    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:  # noqa: ARG002
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        if cell not in self.bishop:
            return set()

        reachable: set[Cell] = set()
        reachable.update(self.bishop)
        reachable.discard(cell)

        return reachable

    def get_regions(self) -> list[set[Cell]]:
        """Get the regions defined by the bishop constraint.

        Returns:
            list[set[Cell]]: A list of sets of cells representing the regions.
        """
        return [self.bishop]
