from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell


class CloneConstraint(BaseConstraint):
    """A class representing a clone constraint for Sudoku cells."""

    def __init__(self, clone_cells: set[Cell]) -> None:
        """Initialize the clone constraint with a list of cells.

        Args:
            clone_cells (set[Cell]): The list of cells to apply constraints to.
        """
        super().__init__(ConstraintType.CLONE)
        self.clone_cells = clone_cells
        for cell in self.clone_cells:
            cell.add_clones(self.clone_cells)

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> CloneConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "clone", "cells": ["a1", "a2", ...]}

        Returns:
            CloneConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cells" not in data:
            msg = "Clone constraint requires 'cells' field"
            raise ValueError(msg)

        positions: set[str] = set(data["cells"])
        cells: set[Cell] = {board.get_cell(pos=pos) for pos in positions}

        return cls(cells)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "cells": [cell.pos for cell in self.clone_cells],
        }

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the clone constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            set[Cell]: A set of cells that do not satisfy the clone constraint.

        """
        values: set[int] = set()
        for cell in self.clone_cells:
            if cell.value is not None:
                values.add(cell.value)
        if len(values) > 1:
            self._logger.debug(
                f"Clone constraint violated in cells {self.clone_cells}",
            )
        return self.clone_cells if len(values) > 1 else set()

    @override
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
        for cell in self.clone_cells:
            values &= cell.candidates
        for i in range(1, board.size + 1):
            if i not in values:
                for cell in self.clone_cells:
                    eliminated |= cell.eliminate_candidate(i)
                    # HACK: gestion de la mémoire de ouf avec des pointeurs
        if eliminated:
            self._logger.debug(
                f"Eliminated due to clone cells {self.clone_cells}",
            )
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
        if cell not in self.clone_cells:
            return set()

        reachable: set[Cell] = set()
        for clone_cell in self.clone_cells:
            reachable |= clone_cell.reachable_cells
        reachable -= self.clone_cells

        return reachable

    @override
    def deep_copy(self) -> CloneConstraint:
        """Create a deep copy of the constraint.

        Returns:
            CloneConstraint: A deep copy of the constraint.
        """
        return CloneConstraint(self.clone_cells.copy())

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        cells_repr = ", ".join(c.pos for c in self.clone_cells)
        return f"CloneConstraint([{cells_repr}])"
