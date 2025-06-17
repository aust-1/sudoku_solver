from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from sudoku.solver import BishopConstraint, PalindromeConstraint, Solver

if TYPE_CHECKING:
    from sudoku.models import Board, Cell


class SudokuGUI:
    """Simple PyGame interface to visualise a Sudoku board and candidates."""

    def __init__(self, board: Board, size: int = 60) -> None:
        """Initialise the Sudoku GUI.

        Args:
            board (Board): The Sudoku board to display.
            size (int, optional): The size of each cell in pixels. Defaults to 60.
        """
        self.board = board
        self.size = size
        self.button_height = int(size / 2)
        pygame.init()
        self.screen = pygame.display.set_mode(
            (size * board.size, size * board.size + self.button_height + 20),
        )
        pygame.display.set_caption("Sudoku")
        self.value_font = pygame.font.SysFont(None, int(size / 1.5))
        self.candidate_font = pygame.font.SysFont(None, int(size / 3))
        self.button_font = pygame.font.SysFont(None, int(self.button_height * 0.8))
        self.highlighted_cells: set[Cell] = set()
        self.running = True

    def _get_cell_at_pos(self, pos: tuple[int, int]) -> Cell | None:
        """Return the cell at the given screen position, if any."""
        x, y = pos
        if x >= self.size * self.board.size or y >= self.size * self.board.size:
            return None
        row = y // self.size
        col = x // self.size
        return self.board.get_cell(row, col)

    def _draw_highlights(self) -> None:
        """Highlight currently selected cells."""
        if not self.highlighted_cells:
            return
        highlight = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        highlight.fill((255, 255, 0, 80))
        for cell in self.highlighted_cells:
            rect = pygame.Rect(
                cell.col * self.size,
                cell.row * self.size,
                self.size,
                self.size,
            )
            self.screen.blit(highlight, rect)

    def _draw_line(
        self,
        line: list[Cell],
        color: tuple[int, int, int, int],
        width: int,
    ) -> None:
        """Draw a line on the Sudoku board.

        Args:
            line (list[Cell]): The line to draw.
            color (tuple[int, int, int, int]): The color of the line.
            width (int): The width of the line.
        """
        points = [
            (
                cell.col * self.size + self.size / 2,
                cell.row * self.size + self.size / 2,
            )
            for cell in line
        ]
        surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.lines(
            surf,
            color,
            closed=False,
            points=points,
            width=width,
        )
        self.screen.blit(surf, (0, 0))

    @staticmethod
    def _order_diagonal(cells: set[Cell]) -> list[Cell]:
        """Return cells ordered by diagonal adjacency.

        Args:
            cells (set[Cell]): The cells to order.

        Returns:
            list[Cell]: The ordered cells.
        """
        if not cells:
            return []

        neighbors: dict[Cell, set[Cell]] = {
            cell: {
                other
                for other in cells
                if abs(cell.row - other.row) == 1 and abs(cell.col - other.col) == 1
            }
            for cell in cells
        }
        start = next(c for c in cells if len(neighbors[c]) == 1)
        ordered = [start]
        visited = {start}
        while len(ordered) < len(cells):
            last = ordered[-1]
            nxt = next((n for n in neighbors[last] if n not in visited), None)
            if nxt is None:
                break
            ordered.append(nxt)
            visited.add(nxt)

        if len(ordered) < len(cells):
            ordered.extend(
                sorted(
                    [c for c in cells if c not in visited],
                    key=lambda x: (x.row, x.col),
                ),
            )
        return ordered

    def _draw_constraints(self) -> None:
        """Draw the constraints on the board."""
        for constraint in self.board.constraints:
            if isinstance(constraint, PalindromeConstraint):
                self._draw_line(
                    constraint.palindrome_cells,
                    (0, 140, 255, 120),
                    5,
                )
            elif isinstance(constraint, BishopConstraint):
                self._draw_line(
                    self._order_diagonal(constraint.bishop_cells),
                    (0, 130, 255, 255),
                    2,
                )
        # TODO: even odd constraints, killer constraints

    def _draw_grid(self) -> None:
        """Draw the Sudoku grid."""
        for i in range(self.board.size + 1):
            width = 3 if i % 3 == 0 else 1
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (0, i * self.size),
                (self.board.size * self.size, i * self.size),
                width,
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (i * self.size, 0),
                (i * self.size, self.board.size * self.size),
                width,
            )

    def _draw_values(self) -> None:
        """Draw the values in the Sudoku grid."""
        for r in range(self.board.size):
            for c in range(self.board.size):
                cell = self.board.get_cell(r, c)
                x = c * self.size
                y = r * self.size
                if cell.value is not None:
                    surf = self.value_font.render(str(cell.value), 1, (0, 0, 0))
                    rect = surf.get_rect(center=(x + self.size / 2, y + self.size / 2))
                    self.screen.blit(surf, rect)
                else:
                    for idx in range(1, self.board.size + 1):
                        row = (idx - 1) // 3
                        col = (idx - 1) % 3
                        if idx in cell.candidates:
                            surf = self.candidate_font.render(
                                str(idx),
                                1,
                                (100, 100, 100),
                            )
                            rect = surf.get_rect(
                                center=(
                                    x + (col + 0.5) * self.size / 3,
                                    y + (row + 0.5) * self.size / 3,
                                ),
                            )
                            self.screen.blit(surf, rect)

    def _draw_board(self) -> None:
        """Draw the entire Sudoku board."""
        self.screen.fill((255, 255, 255))
        self._draw_grid()
        self._draw_constraints()
        self._draw_values()
        self._draw_highlights()

    def _draw_step_button(self, rect: pygame.Rect) -> None:
        """Draw the step button."""
        pygame.draw.rect(self.screen, (200, 200, 200), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        text = self.button_font.render("Step", 1, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_run_button(self, rect: pygame.Rect) -> None:
        """Draw the run button."""
        pygame.draw.rect(self.screen, (200, 200, 200), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        text = self.button_font.render("Run", 1, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=rect.center))

    def run(self) -> None:
        """Run the Sudoku GUI."""
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cell = self._get_cell_at_pos(event.pos)
                    if cell:
                        self.highlighted_cells = {cell} | set(cell.reachable_cells)
            self._draw_board()
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

    def run_stepwise(self, solver: Solver) -> None:
        """Run the GUI and advance the solver one step at a time on button press.

        Args:
            solver (Solver): The Sudoku solver instance.
        """
        clock = pygame.time.Clock()
        button_rect = pygame.Rect(
            self.size * 3,
            self.size * self.board.size + 10,
            self.size * 3,
            self.button_height,
        )
        forward_button_rect = pygame.Rect(
            self.size * 6,
            self.size * self.board.size + 10,
            self.size * 3,
            self.button_height,
        )
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(
                    event.pos,
                ):
                    solver.apply(self.board)
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and forward_button_rect.collidepoint(event.pos)
                ):
                    solver.solve(self.board)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cell = self._get_cell_at_pos(event.pos)
                    if cell:
                        self.highlighted_cells = {cell} | set(cell.reachable_cells)
                    else:
                        self.highlighted_cells.clear()
            self._draw_board()
            self._draw_step_button(button_rect)
            self._draw_run_button(forward_button_rect)
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()


# TODO: add list des cellules en higlligth qui sont cochées décochées
