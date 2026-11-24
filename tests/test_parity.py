from __future__ import annotations

import json
from pathlib import Path

import pytest

from models import Board
from solver.constraints import ParityConstraint
from solver.strategies import ConstraintStrategy

ROOT = Path(__file__).resolve().parent.parent


def _load(rest: object) -> Board:
    return Board.from_dict({
        "size": 9,
        "cells": {},
        "constraints": [{"type": "parity", "cell": "a1", "rest": rest}],
    })


@pytest.mark.parametrize(
    ("rest", "expected"),
    [(1, [1, 3, 5, 7, 9]), ("1", [1, 3, 5, 7, 9]), (0, [2, 4, 6, 8]), ("0", [2, 4, 6, 8])],
)
def test_parity_from_dict_accepts_int_and_string(rest: object, expected: list[int]) -> None:
    board = _load(rest)
    (constraint,) = board.constraints
    assert isinstance(constraint, ParityConstraint)
    assert constraint.rest == int(str(rest))
    ConstraintStrategy().apply(board)
    assert sorted(board.get_cell(pos="a1").candidates) == expected


@pytest.mark.parametrize("rest", [2, -1, "2", "odd", None, True, 1.0])
def test_parity_from_dict_rejects_invalid_rest(rest: object) -> None:
    with pytest.raises(ValueError, match="must be 0 \\(even\\) or 1 \\(odd\\)"):
        _load(rest)


def test_parity_to_dict_exports_integer() -> None:
    board = _load("1")
    (constraint,) = board.constraints
    assert constraint.to_dict()["rest"] == 1


@pytest.mark.parametrize("name", ["board.json", "board.example.json"])
def test_example_files_use_integer_parity(name: str) -> None:
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    parity = [c for c in data["constraints"] if c["type"] == "parity"]
    assert parity
    assert all(isinstance(c["rest"], int) for c in parity)
