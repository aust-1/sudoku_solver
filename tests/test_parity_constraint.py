from __future__ import annotations

import pytest

from models import Board
from solver.constraints.even_odd import ParityConstraint


def test_from_dict_converts_string_rest_to_int() -> None:
    board = Board(9)
    data = {"type": "parity", "cell": "a1", "rest": "1"}
    constraint = ParityConstraint.from_dict(board, data)
    assert constraint.rest == 1
    assert isinstance(constraint.rest, int)


def test_from_dict_rejects_invalid_rest() -> None:
    board = Board(9)
    with pytest.raises(ValueError, match=r"0 \(even\) or 1"):
        ParityConstraint.from_dict(board, {"type": "parity", "cell": "a1", "rest": "2"})
    with pytest.raises(ValueError, match="integer"):
        ParityConstraint.from_dict(board, {"type": "parity", "cell": "a1", "rest": "x"})


def test_eliminate_keeps_odd_candidates_when_rest_is_1() -> None:
    board = Board(9)
    data = {"type": "parity", "cell": "a1", "rest": 1}
    constraint = ParityConstraint.from_dict(board, data)
    eliminated = constraint.eliminate(board)
    assert eliminated
    cell = board.get_cell(pos="a1")
    candidates = cell.candidates
    assert all(c % 2 == 1 for c in candidates)
    assert 1 in candidates
    assert 2 not in candidates
