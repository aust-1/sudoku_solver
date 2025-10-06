from __future__ import annotations

from typing import TYPE_CHECKING, override

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.structs import ConstraintType

if TYPE_CHECKING:
    from models import Board, Cell
    from utils.gui import SudokuGUI


class KropkiConstraint(BaseConstraint):
    """A class representing a Kropki constraint."""

    def __init__(self, kropki_cell1: Cell, kropki_cell2: Cell, color: str) -> None:
        """Initialize the Kropki constraint.

        Args:
            kropki_cell1 (Cell): The first cell to constrain.
            kropki_cell2 (Cell): The second cell to constrain.
            color (str): The color of the Kropki constraint (black or white).

        Raises:
            ValueError:
                If the cells are not adjacent or if the color is invalid
                (not ``black`` or ``white``).
        """
        super().__init__(ConstraintType.KROPKI)
        self.cell1 = kropki_cell1
        self.cell2 = kropki_cell2

        if (self.cell1.row - self.cell2.row) ** 2 + (
            self.cell1.col - self.cell2.col
        ) ** 2 != 1:
            msg = "Kropki constraint cells must be adjacent."
            raise ValueError(msg)

        if color == "black":
            self.is_black_dot = True
            self.cell1.eliminate_candidate(5)
            self.cell2.eliminate_candidate(5)
            self.cell1.eliminate_candidate(7)
            self.cell2.eliminate_candidate(7)
            self.cell1.eliminate_candidate(9)
            self.cell2.eliminate_candidate(9)
        elif color == "white":
            self.is_black_dot = False
        else:
            msg = f"Invalid Kropki constraint color: {color}. Use 'black' or 'white'."
            raise ValueError(msg)

    @classmethod
    def black(cls, kropki_cells: set[Cell]) -> KropkiConstraint:
        """Create a Kropki constraint with black dot.

        Args:
            kropki_cells (set[Cell]): The cells to constrain.

        Returns:
            KropkiConstraint: The created Kropki constraint.
        """
        return cls(kropki_cells, color="black")

    @classmethod
    def white(cls, kropki_cells: set[Cell]) -> KropkiConstraint:
        """Create a Kropki constraint with white dot.

        Args:
            kropki_cells (set[Cell]): The cells to constrain.

        Returns:
            KropkiConstraint: The created Kropki constraint.
        """
        return cls(kropki_cells, color="white")

    def _is_kropki_valid(self, v1: int, v2: int) -> bool:
        """Check if the Kropki constraint is satisfied for the given values.

        Args:
            v1 (int): The value of the first cell.
            v2 (int): The value of the second cell.

        Returns:
            bool: True if the Kropki constraint is satisfied, False otherwise.
        """
        if self.is_black_dot:
            return v1 == v2 * 2 or v2 == v1 * 2
        return v1 == v2 + 1 or v2 == v1 + 1

    @override
    def check(self, board: Board) -> set[Cell]:
        """Check if the Kropki constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            set[Cell]: A set of cells that do not satisfy the Kropki constraint.
        """
        if (
            self.cell1.value is not None
            and self.cell2.value is not None
            and not self._is_kropki_valid(self.cell1.value, self.cell2.value)
        ):
            return {self.cell1, self.cell2}
        return set()

    @override
    def eliminate(self, board: Board) -> bool:
        """Automatically complete the Kropki constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                ``True`` if at least one candidate was eliminated,
                ``False`` otherwise.
        """
        eliminated = False

        cell1_candidates: set[int] = set(self.cell1.candidates)
        cell2_candidates: set[int] = set(self.cell2.candidates)

        for v1 in cell1_candidates:
            possible = False
            for v2 in cell2_candidates:
                possible |= self._is_kropki_valid(v1, v2)
            if not possible:
                eliminated |= self.cell1.eliminate_candidate(v1)

        for v2 in cell2_candidates:
            possible = False
            for v1 in cell1_candidates:
                possible |= self._is_kropki_valid(v1, v2)
            if not possible:
                eliminated |= self.cell2.eliminate_candidate(v2)
        if eliminated:
            self._logger.debug(
                f"Eliminated due to Kropki {'black' if self.is_black_dot else 'white'}"
                f" in {self.cell1} and {self.cell2}",
            )
        return eliminated

    @override
    def draw(self, gui: SudokuGUI) -> None:
        """Draw this kropki constraint on ``gui``.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        color = (0, 0, 0, 255) if self.is_black_dot else (255, 255, 255, 255)

        gui.draw_circle_between_cells(self.cell1, self.cell2, color)

    @override
    def deep_copy(self) -> KropkiConstraint:
        """Create a deep copy of the constraint.

        Returns:
            KropkiConstraint: A deep copy of the constraint.
        """
        return KropkiConstraint(
            {self.cell1, self.cell2},
            "black" if self.is_black_dot else "white",
        )


# TODO: implement logique quand plusieurs kropki à la suite

# QUESTION: init par set ou deux cells
