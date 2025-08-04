from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint
from sudoku.solver.constraints.clone import CloneConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell

# QUESTION: pas convaincu


class CloneZoneConstraint(BaseConstraint):
    """A class representing a clones constraint for Sudoku cells."""

    def __init__(self, *clone_zones: list[Cell]) -> None:
        """Initialize the clones constraint with a list of cells.

        Args:
            *clone_zones (list[Cell]): The lists of cells to apply constraints to.

        """
        super().__init__()
        self.zones: list[list[Cell]] = []
        for zone in clone_zones:
            self.zones.append(zone)

        self.clone_constraints: list[CloneConstraint] = []
        for i in range(len(self.zones[0])):
            column_cells: set[Cell] = {self.zones[j][i] for j in range(len(self.zones))}
            self.clone_constraints.append(CloneConstraint(column_cells))

    def check(self, board: Board) -> bool:
        """Check if the clones constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            bool: `True` if the constraint is satisfied, `False` otherwise.

        """
        return all(constraint.check(board) for constraint in self.clone_constraints)

    def eliminate(self, board: Board) -> bool:
        """Automatically complete the clones constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.

        """
        self.logger.debug(
            f"Eliminating candidates for {self.__class__.__name__} constraint",
        )
        eliminated = False
        for constraint in self.clone_constraints:
            eliminated |= constraint.eliminate(board)
        return eliminated

    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.

        """
        reachable_cells: set[Cell] = set()
        for constraint in self.clone_constraints:
            reachable_cells.update(constraint.reachable_cells(board, cell))
        return reachable_cells

    def deep_copy(self) -> CloneZoneConstraint:
        """Create a deep copy of the constraint.

        Returns:
            CloneZoneConstraint: A deep copy of the constraint.

        """
        return CloneZoneConstraint(*[zone.copy() for zone in self.zones])
