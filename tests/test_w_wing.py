from __future__ import annotations

from models import Board
from solver.strategies import WWingStrategy


def _w_wing_board() -> Board:
    board = Board(9)
    # 1 is only possible in a1 and a9 on row a: strong link a1-a9 on 1.
    for col in range(1, 8):
        board.get_cell(row=0, col=col).eliminate_candidate(1)
    # e1 sees a1 and e9 sees a9, both bivalue {1, 2}.
    board.get_cell(pos="e1").candidates = {1, 2}
    board.get_cell(pos="e9").candidates = {1, 2}
    return board


def test_w_wing_eliminates_from_cells_seeing_both_wings() -> None:
    board = _w_wing_board()
    assert WWingStrategy().apply(board)
    for col in range(1, 8):
        assert 2 not in board.get_cell(row=4, col=col).candidates


def test_w_wing_keeps_strong_link_row_and_wings() -> None:
    board = _w_wing_board()
    WWingStrategy().apply(board)
    for col in range(9):
        assert 2 in board.get_cell(row=0, col=col).candidates  # noqa: PLR2004
    assert board.get_cell(pos="e1").candidates == {1, 2}
    assert board.get_cell(pos="e9").candidates == {1, 2}
