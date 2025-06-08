from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class CloneConstraint(BaseConstraint):
    """A class representing a clone constraint for Sudoku cells."""

    def __init__(self, clone_cells: set[Cell]) -> None:
        """Initialize the clone constraint with a list of cells.

        Args:
            clone_cells (set[Cell]): The list of cells to apply constraints to.
        """
        self.clone = clone_cells

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the clone constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            bool: `True` if the constraint is satisfied, `False` otherwise.
        """
        values: set[int] = set()
        for cell in self.clone:
            if cell.value is not None:
                values.add(cell.value)
        return len(values) <= 1

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the clone constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        eliminated = False
        values = set(range(1, board.size + 1))
        for cell in self.clone:
            values.intersection_update(cell.candidates)
        for i in range(1, board.size + 1):
            if i not in values:
                for cell in self.clone:
                    eliminated |= cell.eliminate(i)
                    # HACK: gestion de la mémoire de ouf avec des pointeurs
        return eliminated

    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:  # noqa: ARG002
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        if cell not in self.clone:
            return set()

        reachable: set[Cell] = set()
        for clone_cell in self.clone:
            reachable.update(clone_cell.reachable_cells)
        reachable.difference_update(self.clone)

        return reachable
