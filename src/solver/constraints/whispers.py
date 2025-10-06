from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, overload, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class _BaseDiffConstraint(BaseConstraint):
    """A class representing a base difference constraint for Sudoku cells."""

    def __init__(
        self,
        cells: list[Cell],
        diff: int,
        constraint_type: ConstraintType,
    ) -> None:
        """Initialize the difference constraint with a list of cell positions.

        Args:
            cells (list[Cell]): The list of cells to apply constraints to.
            diff (int): The difference value for the constraint.
            constraint_type (ConstraintType): The type of constraint to apply.
        """
        super().__init__(constraint_type)
        self.cells: list[Cell] = cells
        self.diff: int = diff

    @abstractmethod
    @override
    @classmethod
    def from_dict(cls, board: Board, data: dict[str, Any]) -> _BaseDiffConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.

        Returns:
            _BaseDiffConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        msg = "_BaseDiffConstraint.from_dict should not be called directly"
        raise NotImplementedError(msg)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Convert constraint to dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the constraint.
        """
        return {
            "type": self.type.value,
            "cells": [cell.pos for cell in self.cells],
        }

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the difference constraint is satisfied.

        Args:
            board (Board): The Sudoku board to check.

        Returns:
            set[Cell]: A set of cells that do not satisfy the constraint.
        """
        invalid_cells: set[Cell] = set()
        for i in range(len(self.cells) - 1):
            value = self.cells[i].value
            next_value = self.cells[i + 1].value
            if (
                value is not None
                and next_value is not None
                and abs(value - next_value) < self.diff
            ):
                invalid_cells |= {self.cells[i], self.cells[i + 1]}
        return invalid_cells

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the difference constraint on the given board.

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
        eliminated: bool = False
        for i, current_cell in enumerate(self.cells):
            prev_cell: Cell | None = None
            next_cell: Cell | None = None

            if i - 1 >= 0:
                prev_cell = self.cells[i - 1]
            if i + 1 < len(self.cells):
                next_cell = self.cells[i + 1]

            if prev_cell:
                eliminated |= self._eliminate_candidates(current_cell, prev_cell)

            if next_cell:
                eliminated |= self._eliminate_candidates(current_cell, next_cell)

            if prev_cell and next_cell and prev_cell in next_cell.reachable_cells:
                eliminated |= self._eliminate_candidates(
                    current_cell,
                    prev_cell,
                    next_cell,
                )

        return eliminated

    @overload
    def _eliminate_candidates(self, cell1: Cell, cell2: Cell) -> bool: ...

    @overload
    def _eliminate_candidates(self, cell1: Cell, cell2: Cell, cell3: Cell) -> bool: ...

    def _eliminate_candidates(
        self,
        cell1: Cell,
        cell2: Cell,
        cell3: Cell | None = None,
    ) -> bool:
        eliminated = False

        if cell3 is None:
            for cand1 in cell1.candidates.copy():
                for cand2 in cell2.candidates.copy():
                    if abs(cand1 - cand2) > self.diff:
                        break
                else:
                    eliminated |= cell1.eliminate_candidate(cand1)

        else:
            for cand1 in cell1.candidates.copy():
                for cand2 in cell2.candidates.copy():
                    for cand3 in cell3.candidates.copy():
                        if (
                            cand2 != cand3
                            and abs(cand1 - cand2) > self.diff
                            and abs(cand1 - cand3) > self.diff
                        ):
                            break
                    else:
                        break
                else:
                    eliminated |= cell1.eliminate_candidate(cand1)

        return eliminated

    @override
    def deep_copy(self) -> _BaseDiffConstraint:
        """Create a deep copy of the constraint.

        Returns:
            _BaseDiffConstraint: A deep copy of the constraint.
        """
        if self.type == ConstraintType.GERMAN:
            return GermanConstraint(self.cells.copy())
        if self.type == ConstraintType.DUTCH:
            return DutchConstraint(self.cells.copy())
        msg = f"Deep copy not implemented for {self.type} constraint"
        raise NotImplementedError(msg)

    @override
    def __repr__(self) -> str:
        """Return string representation of the constraint.

        Returns:
            str: String representation for debugging.
        """
        cells_repr = ", ".join(c.pos for c in self.cells)
        return f"{self.__class__.__name__}([{cells_repr}])"


class GermanConstraint(_BaseDiffConstraint):
    """A class representing a German constraint for Sudoku cells."""

    def __init__(self, german_cells: list[Cell]) -> None:
        """Initialize the German constraint with a list of cells.

        Args:
            german_cells (list[Cell]): The list of cells to apply constraints to.

        """
        super().__init__(german_cells, 5, ConstraintType.GERMAN)

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> GermanConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "german", "cells": ["a1", "a2", ...]}

        Returns:
            GermanConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cells" not in data:
            msg = "German constraint requires 'cells' field"
            raise ValueError(msg)

        positions: list[str] = list(data["cells"])
        cells: list[Cell] = [board.get_cell(pos=pos) for pos in positions]

        return cls(cells)

    @override
    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.

        """
        if cell not in self.cells:
            return set()

        reachable_cells: set[Cell] = set()
        idx = self.cells.index(cell)

        for i, german_cell in enumerate(self.cells):
            if i % 2 != idx % 2:
                reachable_cells.add(german_cell)

        return reachable_cells

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this german constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        gui.draw_line(self.cells, (0, 255, 0, 120), 5)


class DutchConstraint(_BaseDiffConstraint):
    """A class representing a Dutch constraint for Sudoku cells."""

    def __init__(self, dutch_cells: list[Cell]) -> None:
        """Initialize the Dutch constraint with a list of cells.

        Args:
            dutch_cells (list[Cell]): The list of cells to apply constraints to.
        """
        super().__init__(dutch_cells, 5, ConstraintType.DUTCH)

    @classmethod
    @override
    def from_dict(cls, board: Board, data: dict[str, Any]) -> DutchConstraint:
        """Create a constraint instance from dictionary data.

        Args:
            board (Board): The Sudoku board the constraint applies to.
            data (dict[str, Any]): Dictionary containing constraint configuration.
                Expected format: {"type": "dutch", "cells": ["a1", "a2", ...]}

        Returns:
            DutchConstraint: New constraint instance.

        Raises:
            ValueError: If data format is invalid.
        """
        if "cells" not in data:
            msg = "Dutch constraint requires 'cells' field"
            raise ValueError(msg)

        positions: list[str] = list(data["cells"])
        cells: list[Cell] = [board.get_cell(pos=pos) for pos in positions]

        return cls(cells)

    @override
    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.
        """
        if cell not in self.cells:
            return set()

        reachable_cells: set[Cell] = set()
        idx = self.cells.index(cell)

        if idx > 0:
            reachable_cells.add(self.cells[idx - 1])
        if idx < len(self.cells) - 1:
            reachable_cells.add(self.cells[idx + 1])

        return reachable_cells

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this dutch constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        gui.draw_line(self.cells, (255, 154, 0, 120), 4)
