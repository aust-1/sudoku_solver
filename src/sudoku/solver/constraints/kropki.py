from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.constraints.base_constraint import BaseConstraint

if TYPE_CHECKING:
    from sudoku.models import Board, Cell
    from sudoku.utils.gui import SudokuGUI


class KropkiConstraint(BaseConstraint):
    """A class representing a Kropki constraint."""

    def __init__(self, kropki_cells: set[Cell], color: str) -> None:
        """Initialize the Kropki constraint.

        Args:
            kropki_cells (set[Cell]): The cells to constrain.
            color (str): The color of the Kropki constraint (black or white).

        Raises:
            ValueError: If the cells are not adjacent.
            ValueError: If the color is not 'black' or 'white'.
        """
        super().__init__()
        self.cell1, self.cell2 = kropki_cells

        if (abs(self.cell1.row - self.cell2.row) == 1) == (
            abs(self.cell1.col - self.cell2.col) == 1
        ):
            msg = "Kropki constraint cells must be adjacent."
            raise ValueError(msg)

        if color == "black":
            self.is_black_dot = True
            self.cell1.eliminate(5)
            self.cell2.eliminate(5)
            self.cell1.eliminate(7)
            self.cell2.eliminate(7)
            self.cell1.eliminate(9)
            self.cell2.eliminate(9)
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

    def check(self, board: Board) -> bool:  # noqa: ARG002
        """Check if the Kropki constraint is satisfied.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: `True` if the Kropki constraint is satisfied, `False` otherwise.
        """
        return (
            self.cell1.value is None
            or self.cell2.value is None
            or self._is_kropki_valid(self.cell1.value, self.cell2.value)
        )

    def eliminate(self, board: Board) -> bool:  # noqa: ARG002
        """Automatically complete the Kropki constraint on the given board.

        Args:
            board (Board): The Sudoku board to auto-complete.

        Returns:
            bool:
                `True` if at least one candidate was eliminated,
                `False` otherwise.
        """
        eliminated = False

        cell1_candidates: set[int] = set(self.cell1.candidates)
        cell2_candidates: set[int] = set(self.cell2.candidates)

        for v1 in cell1_candidates:
            possible = False
            for v2 in cell2_candidates:
                possible |= self._is_kropki_valid(v1, v2)
            if not possible:
                eliminated |= self.cell1.eliminate(v1)

        for v2 in cell2_candidates:
            possible = False
            for v1 in cell1_candidates:
                possible |= self._is_kropki_valid(v1, v2)
            if not possible:
                eliminated |= self.cell2.eliminate(v2)
        if eliminated:
            self.logger.debug(
                f"Eliminated due to Kropki {'black' if self.is_black_dot else 'white'}"
                f" in {self.cell1} and {self.cell2}",
            )
        return eliminated

    def draw(self, gui: SudokuGUI) -> None:
        """Draw this kropki constraint on `gui` if supported.

        Args:
            gui (SudokuGUI): The GUI to draw on.
        """
        color = (0, 0, 0, 255) if self.is_black_dot else (255, 255, 255, 255)

        gui.draw_circle_between_cells(self.cell1, self.cell2, color)

    def deep_copy(self) -> KropkiConstraint:
        """Create a deep copy of the constraint.

        Returns:
            BaseConstraint: A deep copy of the constraint.
        """
        return KropkiConstraint(
            {self.cell1, self.cell2},
            "black" if self.is_black_dot else "white",
        )


# TODO: implement logique quand plusieurs kropki à la suite

# QUESTION: init par set ou deux cells
