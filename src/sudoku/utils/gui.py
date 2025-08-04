from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from sudoku.models import Board, Cell
    from sudoku.solver import Solver


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

    def draw_line(
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
        # FIXME: à la fin et au début ça doit aller un peu moins loin

    def draw_circle_in_cell(
        self,
        cell: Cell,
        color: tuple[int, int, int, int],
    ) -> None:
        """Draw a circle centred in `cell`.

        Args:
            cell (Cell): The cell to draw on.
            color (tuple[int, int, int, int]): The color of the circle.
        """
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            surf,
            color,
            (self.size // 2, self.size // 2),
            self.size // 2 - 5,
        )
        self.screen.blit(surf, (cell.col * self.size, cell.row * self.size))

    def draw_circle_between_cells(
        self,
        cell1: Cell,
        cell2: Cell,
        color: tuple[int, int, int, int],
    ) -> None:
        """Draw a circle between `cell1` and `cell2`.

        Args:
            cell1 (Cell): The first cell.
            cell2 (Cell): The second cell.
            color (tuple[int, int, int, int]): The color of the circle.
        """
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            surf,
            (0, 0, 0, 255),
            (self.size // 2, self.size // 2),
            self.size // 10,
        )
        pygame.draw.circle(
            surf,
            color,
            (self.size // 2, self.size // 2),
            self.size // 10 - 2,
        )
        self.screen.blit(
            surf,
            (
                (cell1.col * self.size + cell2.col * self.size) / 2,
                (cell1.row * self.size + cell2.row * self.size) / 2,
            ),
        )

    def write_text_between_cells(
        self,
        cell1: Cell,
        cell2: Cell,
        text: str,
    ) -> None:
        """Write a text between `cell1` and `cell2`.

        Args:
            cell1 (Cell): The first cell.
            cell2 (Cell): The second cell.
            text (str): The text to write.
        """
        text_to_render = pygame.font.SysFont(None, 40).render(text, 1, [0, 0, 0])
        self.screen.blit(
            text_to_render,
            (
                (cell1.col * self.size + cell2.col * self.size) / 2,
                (cell1.row * self.size + cell2.row * self.size) / 2,
            ),
        )

    def draw_square(
        self,
        cell: Cell,
        color: tuple[int, int, int, int],
    ) -> None:
        """Draw a square centred in `cell`.

        Args:
            cell (Cell): The cell to draw on.
            color (tuple[int, int, int, int]): The color of the square.
        """
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        margin = 6
        pygame.draw.rect(
            surf,
            color,
            pygame.Rect(margin, margin, self.size - 2 * margin, self.size - 2 * margin),
        )
        self.screen.blit(surf, (cell.col * self.size, cell.row * self.size))

    @staticmethod
    def _draw_dashed_line(
        surf: pygame.Surface,
        start: tuple[int, int],
        end: tuple[int, int],
        color: tuple[int, int, int, int],
    ) -> None:
        """Draw a dashed line on `surf` from `start` to `end`.

        Args:
            surf (pygame.Surface): The surface to draw on.
            start (tuple[int, int]): The starting point of the line.
            end (tuple[int, int]): The ending point of the line.
            color (tuple[int, int, int, int]): The color of the line.
        """
        width = 1
        dash_length = 5
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        distance = max(abs(dx), abs(dy))
        for i in range(0, distance, dash_length * 2):
            start_pos = (
                x1 + dx * i // distance,
                y1 + dy * i // distance,
            )
            end_pos = (
                x1 + dx * min(i + dash_length, distance) // distance,
                y1 + dy * min(i + dash_length, distance) // distance,
            )
            pygame.draw.line(surf, color, start_pos, end_pos, width)

    def draw_killer_cage(
        self,
        cells: set[Cell],
        total_sum: int,
        color: tuple[int, int, int, int],
    ) -> None:
        """Draw a killer cage around `cells` with the sum displayed.

        Args:
            cells (set[Cell]): The cells to draw the cage around.
            total_sum (int): The total sum of the cage.
            color (tuple[int, int, int, int]): The color of the cage.
        """
        surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        margin = 3
        for cell in cells:
            x = cell.col * self.size
            y = cell.row * self.size
            rect = pygame.Rect(x, y, self.size, self.size)
            neighbors = {
                "top": (
                    self.board.get_cell(cell.row - 1, cell.col)
                    if cell.row > 0
                    else None
                ),
                "bottom": (
                    self.board.get_cell(cell.row + 1, cell.col)
                    if cell.row < self.board.size - 1
                    else None
                ),
                "left": (
                    self.board.get_cell(cell.row, cell.col - 1)
                    if cell.col > 0
                    else None
                ),
                "right": (
                    self.board.get_cell(cell.row, cell.col + 1)
                    if cell.col < self.board.size - 1
                    else None
                ),
            }
            if neighbors["top"] not in cells:
                self._draw_dashed_line(
                    surf,
                    (rect.left + margin, rect.top + margin),
                    (rect.right - margin, rect.top + margin),
                    color,
                )
            if neighbors["right"] not in cells:
                self._draw_dashed_line(
                    surf,
                    (rect.right - margin, rect.top + margin),
                    (rect.right - margin, rect.bottom - margin),
                    color,
                )
            if neighbors["bottom"] not in cells:
                self._draw_dashed_line(
                    surf,
                    (rect.left + margin, rect.bottom - margin),
                    (rect.right - margin, rect.bottom - margin),
                    color,
                )
            if neighbors["left"] not in cells:
                self._draw_dashed_line(
                    surf,
                    (rect.left + margin, rect.top + margin),
                    (rect.left + margin, rect.bottom - margin),
                    color,
                )
        self.screen.blit(surf, (0, 0))

        top_left = min(cells, key=lambda c: (c.row, c.col))
        text = self.candidate_font.render(str(total_sum), 1, [0, 0, 0])
        self.screen.blit(
            text,
            (top_left.col * self.size + 2, top_left.row * self.size + 2),
        )

    @staticmethod
    def order_diagonal(cells: set[Cell]) -> list[Cell]:
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
            constraint.draw(self)

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
# TODO: affichage des codes de chaque ligne et collones
# HACK: lignes de bishop qui vont jusqu'au bord
# HACK: couleur différente en fonction de déduction ou don
