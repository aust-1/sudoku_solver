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
            board: The Sudoku board.

        Returns:
            ``True`` if any candidates were eliminated, ``False`` otherwise.
        """
        self.logger.info("XWingStrategy running")
        moved = False
        digits = range(1, board.size + 1)

        regions = [r for r in board.regions if len(r) == board.size]

        for digit in digits:
            candidate_pairs: list[tuple[Cell, Cell]] = []
            for region in regions:
                cells = [
                    cell
                    for cell in region
                    if not cell.is_filled() and digit in cell.candidates
                ]
                if len(cells) == 2:  # noqa: PLR2004
                    candidate_pairs.append((cells[0], cells[1]))

            for i in range(len(candidate_pairs)):
                (a1, b1) = candidate_pairs[i]
                for j in range(i + 1, len(candidate_pairs)):
                    (a2, b2) = candidate_pairs[j]

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
                        }
                    )
                    for cell in targets:
                        if cell.eliminate(digit):
                            moved = True

        return moved
