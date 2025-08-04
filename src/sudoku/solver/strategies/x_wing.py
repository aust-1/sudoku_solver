from __future__ import annotations

from typing import TYPE_CHECKING

from sudoku.solver.solver import Solver

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class XWingStrategy(Solver):
    """Eliminate candidates using the X-Wing technique."""

    def apply(self, board: Board) -> bool:
        """Apply the X-Wing strategy to the board.

        Args:
            board (Board): The Sudoku board.

        Returns:
            bool: ``True`` if any candidates were eliminated, ``False`` otherwise.

        """
        self.logger.debug("XWingStrategy running")
        moved = False

        for digit in range(1, board.size + 1):
            strong_links: set[tuple[Cell, Cell]] = set()
            for region in (r for r in board.regions.values() if len(r) == board.size):
                cells = [
                    cell
                    for cell in region
                    if not cell.is_filled() and digit in cell.candidates
                ]
                if len(cells) == 2:  # noqa: PLR2004
                    strong_links.add((cells[0], cells[1]))

            for a1, b1 in strong_links:
                for a2, b2 in strong_links:
                    targets1 = a1.reachable_cells.copy()
                    targets2 = b1.reachable_cells.copy()

                    if a2 in a1.reachable_cells and b2 in b1.reachable_cells:
                        targets1.intersection_update(a2.reachable_cells)
                        targets2.intersection_update(b2.reachable_cells)
                    elif a2 in b1.reachable_cells and b2 in a1.reachable_cells:
                        targets1.intersection_update(b2.reachable_cells)
                        targets2.intersection_update(a2.reachable_cells)
                    else:
                        continue

                    targets = (targets1.union(targets2)).difference(
                        {
                            a1,
                            b1,
                            a2,
                            b2,
                        },
                    )
                    for cell in targets:
                        if cell.eliminate(digit):
                            moved = True
                            self.logger.debug(
                                f"({a1.row}, {a1.col}), ({b1.row}, {b1.col}), "
                                f"({a2.row}, {a2.col}), ({b2.row}, {b2.col})",
                            )

        return moved
