from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class BishopConstraint(BaseConstraint):
    """A class representing a bishop's movement constraint."""

    def __init__(self, bishop_cells: set[Cell]) -> None:
        """Initialize the bishop's movement constraint.

        Args:
            bishop_cells (set[Cell]): The cells that the bishop can move to.

        """
        super().__init__(ConstraintType.BISHOP)
        self.bishop_cells = bishop_cells

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the bishop's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            set[Cell]:
                A set of cells that do not satisfy the bishop's movement constraint.
        """
        cells_by_value: dict[int, set[Cell]] = {}
        for cell in self.bishop_cells:
            if cell.value is not None:
                cells_by_value.setdefault(cell.value, set()).add(cell)

        invalid_cells: set[Cell] = set()
        for value, cells in cells_by_value.items():
            if len(cells) > 1:
                self._logger.debug(
                    f"Bishop constraint violated for value {value} "
                    f"in cells: {[(c.row, c.col) for c in cells]}",
                )
                invalid_cells |= cells

        return invalid_cells

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the bishop's movement constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.

        """
        return False

    @override
    def reachable_cells(self, board: Board, cell: Cell) -> set[Cell]:
        """Get the reachable cells based on the constraint.

        Args:
            board (Board): The Sudoku board.
            cell (Cell): The cell.

        Returns:
            set[Cell]: A set of reachable cells.

        """
        if cell not in self.bishop_cells:
            return set()

        reachable: set[Cell] = set()
        reachable |= self.bishop_cells
        reachable.discard(cell)

        return reachable

    @override
    def get_regions(self, board: Board) -> dict[str, set[Cell]]:
        """Get the regions defined by the constraint.

        Args:
            board (Board): The Sudoku board.

        Returns:
            dict[str,set[Cell]]: A dictionary of sets of cells representing the regions.

        """
        idx = 1
        while f"bishop_{idx}" in board.regions:
            idx += 1
        return {f"bishop_{idx}": self.bishop_cells}

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this bishop constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.

        """
        gui.draw_line(
            gui.order_diagonal(self.bishop_cells),
            (0, 130, 255, 255),
            2,
        )

    @override
    def deep_copy(self) -> BishopConstraint:
        """Create a deep copy of the constraint.

        Returns:
            BishopConstraint: A deep copy of the constraint.

        """
        return BishopConstraint(self.bishop_cells.copy())
