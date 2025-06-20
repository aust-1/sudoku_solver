from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell
    from sudoku.utils.gui import SudokuGUI


class BishopConstraint(BaseConstraint):
    """A class representing a bishop's movement constraint."""

    def __init__(self, bishop_cells: set[Cell]) -> None:
        """Initialize the bishop's movement constraint."""
        super().__init__()
        self.bishop_cells = bishop_cells

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the bishop's movement is valid.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: `True` if the bishop's movement is valid, `False` otherwise.
        """
        values: set[int] = set()
        for cell in self.bishop_cells:
            if cell.value is not None:
                if cell.value in values:
                    self.logger.debug(
                        f"Bishop constraint violated at cell ({cell.row}, {cell.col})"
                        f" with value {cell.value}",
                    )
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
        self.logger.debug(
            f"Eliminating candidates for {self.__class__.__name__} constraint",
        )
        eliminated = False
        for cell in self.bishop_cells:
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
        if cell not in self.bishop_cells:
            return set()

        reachable: set[Cell] = set()
        reachable.update(self.bishop_cells)
        reachable.discard(cell)

        return reachable

    def get_regions(self, board: Board) -> list[set[Cell]]:  # noqa: ARG002
        """Get the regions defined by the constraint.

        Args:
            board (Board): The Sudoku board.

        Returns:
            list[set[Cell]]: A list of sets of cells representing the regions.
        """
        return [self.bishop_cells]

    def draw(self, gui: SudokuGUI) -> None:
        """Draw this bishop constraint on `gui` if supported.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        gui.draw_line(
            gui.order_diagonal(self.bishop_cells),
            (0, 130, 255, 255),
            2,
        )

    def deep_copy(self) -> BishopConstraint:
        """Create a deep copy of the constraint.

        Returns:
            BaseConstraint: A deep copy of the constraint.
        """
        return BishopConstraint(self.bishop_cells.copy())
