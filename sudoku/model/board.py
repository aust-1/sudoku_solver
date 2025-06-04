from __future__ import annotations
"""Module containing the :class:`Board` model."""


from dataclasses import dataclass
from typing import Iterable, List

from .cell import Cell


class Board:
    """Represents the Sudoku board as a 9x9 grid of cells."""

    def __init__(self):
        self.grid: List[List[Cell]] = [
            [Cell(r, c) for c in range(9)] for r in range(9)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]

    def get_row(self, r: int) -> List[Cell]:
        return list(self.grid[r])

    def get_col(self, c: int) -> List[Cell]:
        return [self.grid[r][c] for r in range(9)]

    def get_box(self, box_index: int) -> List[Cell]:
        start_r = (box_index // 3) * 3
        start_c = (box_index % 3) * 3
        return [
            self.grid[r][c]
            for r in range(start_r, start_r + 3)
            for c in range(start_c, start_c + 3)
        ]

    def get_all_cells(self) -> Iterable[Cell]:
        for row in self.grid:
            for cell in row:
                yield cell

    def is_valid(self) -> bool:
        def region_valid(cells: Iterable[Cell]) -> bool:
            values = [c.value for c in cells if c.is_filled()]
            return len(values) == len(set(values))

        return all(
            region_valid(self.get_row(g)) and region_valid(self.get_col(g)) and region_valid(self.get_box(g))
            for g in range(9)
        )

    def is_solved(self) -> bool:
        return all(cell.is_filled() for cell in self.get_all_cells())

    def load_from(self, input_str: str) -> None:
        digits = [d for d in input_str if d.isdigit()]
        for idx, d in enumerate(digits[:81]):
            if d != '0':
                r, c = divmod(idx, 9)
                self.grid[r][c].set_value(int(d))

    #TODO: Load stylé fichier, interface ?

    def __str__(self) -> str:
        lines = []
        for r in range(9):
            row = ' '.join(str(self.grid[r][c]) for c in range(9))
            lines.append(row)
        return '\n'.join(lines)

    def deep_copy(self) -> Board:
        board = Board()
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                copy_cell = board.grid[r][c]
                copy_cell.value = cell.value
                copy_cell.candidates = set(cell.candidates)
        return board

    def copy_values_from(self, other: Board) -> None:
        for r in range(9):
            for c in range(9):
                self.grid[r][c].value = other.grid[r][c].value
                self.grid[r][c].candidates = set(other.grid[r][c].candidates)
