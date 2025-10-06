from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.clone import CloneConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class PalindromeConstraint(BaseConstraint):
    """A class representing a palindrome constraint for Sudoku cells."""

    def __init__(self, palindrome_cells: list[Cell]) -> None:
        """Initialize the palindrome constraint with a list of cells.

        Args:
            palindrome_cells (list[Cell]): The list of cells to apply constraints to.
        """
        super().__init__(ConstraintType.PALINDROME)
        self.palindrome_cells: list[Cell] = palindrome_cells
        self.clone_constraints: list[CloneConstraint] = []
        for i in range(len(palindrome_cells) // 2):
            self.clone_constraints.append(
                CloneConstraint({palindrome_cells[i], palindrome_cells[-(i + 1)]}),
            )

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> PalindromeConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "palindrome", "cells": ["a1", "a2", ...]}

        Returns:
            PalindromeConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cells" not in data:
            msg = "Palindrome constraint requires 'cells' field"
            raise ValueError(msg)

        positions: list[str] = list(data["cells"])
        cells: list[Cell] = [board.get_cell(pos=pos) for pos in positions]

        return cls(cells)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "cells": [cell.pos for cell in self.palindrome_cells],
        }

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the palindrome constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            set[Cell]: A set of cells that do not satisfy the palindrome constraint.
        """
        return {
            cell
            for constraint in self.clone_constraints
            for cell in constraint.check(board)
        }

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the palindrome constraint on the given board.

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
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this palindrome constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        gui.draw_line(self.palindrome_cells, (0, 140, 255, 120), 5)

    @override
    def deep_copy(self) -> PalindromeConstraint:
        """Create a deep copy of the constraint.

        Returns:
            PalindromeConstraint: A deep copy of the constraint.
        """
        return PalindromeConstraint(self.palindrome_cells.copy())

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        cells_repr = ", ".join(c.pos for c in self.palindrome_cells)
        return f"PalindromeConstraint([{cells_repr}])"
