from __future__ import annotations

import pygame

from sudoku.solver import Solver

from sudoku.models import Board


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
            (size * 9, size * 9 + self.button_height + 20)
        )
        pygame.display.set_caption("Sudoku")
        self.value_font = pygame.font.SysFont(None, int(size / 1.5))
        self.candidate_font = pygame.font.SysFont(None, int(size / 3))
        self.button_font = pygame.font.SysFont(None, int(self.button_height * 0.8))
        self.running = True

    def draw_grid(self) -> None:
        """Draw the Sudoku grid."""
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (0, i * self.size),
                (9 * self.size, i * self.size),
                width,
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (i * self.size, 0),
                (i * self.size, 9 * self.size),
                width,
            )

    def draw_values(self) -> None:
        """Draw the values in the Sudoku grid."""
        for r in range(9):
            for c in range(9):
                cell = self.board.get_cell(r, c)
                x = c * self.size
                y = r * self.size
                if cell.value is not None:
                    surf = self.value_font.render(str(cell.value), True, (0, 0, 0))
                    rect = surf.get_rect(center=(x + self.size / 2, y + self.size / 2))
                    self.screen.blit(surf, rect)
                else:
                    for idx in range(1, 10):
                        row = (idx - 1) // 3
                        col = (idx - 1) % 3
                        if idx in cell.candidates:
                            surf = self.candidate_font.render(
                                str(idx), True, (100, 100, 100)
                            )
                            rect = surf.get_rect(
                                center=(
                                    x + (col + 0.5) * self.size / 3,
                                    y + (row + 0.5) * self.size / 3,
                                )
                            )
                            self.screen.blit(surf, rect)

    def draw_board(self) -> None:
        """Draw the entire Sudoku board."""
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_values()

    def _draw_step_button(self, rect: pygame.Rect) -> None:
        """Draw the step button."""
        pygame.draw.rect(self.screen, (200, 200, 200), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        text = self.button_font.render("Step", True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_run_button(self, rect: pygame.Rect) -> None:
        """Draw the run button."""
        pygame.draw.rect(self.screen, (200, 200, 200), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        text = self.button_font.render(">>", True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=rect.center))

    def run(self) -> None:
        """Run the Sudoku GUI."""
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw_board()
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

    def run_stepwise(self, solver: "Solver") -> None:
        """Run the GUI and advance the solver one step at a time on button press."""
        clock = pygame.time.Clock()
        button_rect = pygame.Rect(
            self.size * 3, self.size * 9 + 10, self.size * 3, self.button_height
        )
        forward_button_rect = pygame.Rect(
            self.size * 6, self.size * 9 + 10, self.size * 3, self.button_height
        )
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(
                    event.pos
                ):
                    solver.apply(self.board)
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and forward_button_rect.collidepoint(event.pos)
                ):
                    solver.solve(self.board)
            self.draw_board()
            self._draw_step_button(button_rect)
            self._draw_run_button(forward_button_rect)
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()
