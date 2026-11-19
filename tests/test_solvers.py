"""Regression tests for the solvers on classic grids."""

from __future__ import annotations

from models import Board
from solver import CompositeSolver
from solver.backtracking import BacktrackingSolver
from solver.strategies import EliminationStrategy, HiddenSingleStrategy

PUZZLE = (
    "530070000"
    "600195000"
    "098000060"
    "800060003"
    "400803001"
    "700020006"
    "060000280"
    "000419005"
    "000080079"
)
SOLUTION = (
    "534678912"
    "672195348"
    "198342567"
    "859761423"
    "426853791"
    "713924856"
    "961537284"
    "287419635"
    "345286179"
)
HARD_PUZZLE = (
    "000000010"
    "400000000"
    "020000000"
    "000050407"
    "008000300"
    "001090000"
    "300400200"
    "050100000"
    "000806000"
)


def _digits(board: Board) -> str:
    return "".join(str(cell.value or 0) for cell in board.get_all_cells())


def _board(puzzle: str) -> Board:
    board = Board(9)
    board.load_from_string(puzzle)
    return board


def test_composite_solves_classic_puzzle() -> None:
    board = _board(PUZZLE)
    assert CompositeSolver().solve(board)
    assert board.is_solved()
    assert _digits(board) == SOLUTION


def test_backtracking_solves_classic_puzzle() -> None:
    board = _board(PUZZLE)
    assert BacktrackingSolver().apply(board)
    assert board.is_solved()
    assert _digits(board) == SOLUTION


def test_hard_puzzle_is_solved() -> None:
    board = _board(HARD_PUZZLE)
    assert CompositeSolver().solve(board)
    assert board.is_solved()
    for idx, digit in enumerate(HARD_PUZZLE):
        if digit != "0":
            assert _digits(board)[idx] == digit


def test_elimination_removes_placed_digit_from_peers() -> None:
    board = Board(9)
    board.get_cell(pos="e5").value = 4
    # The setter already propagates: a second pass has nothing left to do.
    assert not EliminationStrategy().apply(board)
    for pos in ("e1", "a5", "d4"):
        assert 4 not in board.get_cell(pos=pos).candidates  # noqa: PLR2004


def test_hidden_single_places_only_possible_digit() -> None:
    board = Board(9)
    # 7 can only go in a1 on row a.
    for col in range(1, 9):
        board.get_cell(row=0, col=col).eliminate_candidate(7)
    assert HiddenSingleStrategy().apply(board)
    assert board.get_cell(pos="a1").value == 7  # noqa: PLR2004
