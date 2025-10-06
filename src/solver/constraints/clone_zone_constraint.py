from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.clone import CloneConstraint

if TYPE_CHECKING:
    from models import Board, Cell

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

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> CloneZoneConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "clone_zone", "zones": [["a1", "a2"], ["b1", "b2"]]}

        Returns:
            CloneZoneConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "zones" not in data:
            msg = "CloneZone constraint requires 'zones' field"
            raise ValueError(msg)

        zones = [[board.get_cell(pos=pos) for pos in zone] for zone in data["zones"]]

        return cls(*zones)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "zones": [[cell.pos for cell in zone] for zone in self.zones],
        }

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the clones constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            set[Cell]: A set of cells that do not satisfy the clones constraint.
        """
        return {
            cell
            for constraint in self.clone_constraints
            for cell in constraint.check(board)
        }

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the clones constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        self._logger.debug(
            f"Eliminating candidates for {self.__class__.__name__} constraint",
        )
        eliminated = False
        for constraint in self.clone_constraints:
            eliminated |= constraint.eliminate(board)
        return eliminated

    @override
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
            reachable_cells |= constraint.reachable_cells(board, cell)
        return reachable_cells

    @override
    def deep_copy(self) -> CloneZoneConstraint:
        """Create a deep copy of the constraint.

        Returns:
            CloneZoneConstraint: A deep copy of the constraint.
        """
        return CloneZoneConstraint(*[zone.copy() for zone in self.zones])

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        zones_repr = ", ".join("[" + ", ".join(zone) + "]" for zone in self.zones)
        return f"CloneZoneConstraint({zones_repr})"
