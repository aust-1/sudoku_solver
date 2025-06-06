from __future__ import annotations

import pygame

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
        pygame.init()
        self.screen = pygame.display.set_mode((size * 9, size * 9))
        pygame.display.set_caption("Sudoku")
        self.value_font = pygame.font.SysFont(None, int(size / 1.5))
        self.candidate_font = pygame.font.SysFont(None, int(size / 3))
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
        pygame.display.flip()

    def run(self) -> None:
        """Run the Sudoku GUI."""
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw_board()
            clock.tick(30)
        pygame.quit()
