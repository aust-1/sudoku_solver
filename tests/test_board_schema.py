from __future__ import annotations

import pytest

from models import Board
from utils.exceptions import InvalidSudokuError


def _base_payload() -> dict[str, object]:
    return {"size": 9, "cells": {}, "constraints": []}


def test_from_dict_accepts_constraints_key() -> None:
    board = Board.from_dict(_base_payload())
    assert board.size == 9


def test_from_dict_accepts_legacy_constraint_key() -> None:
    payload = {"size": 9, "cells": {}, "constraint": []}
    board = Board.from_dict(payload)
    assert board.size == 9


def test_from_dict_rejects_invalid_cell_id() -> None:
    payload = _base_payload()
    payload["cells"] = {"z9": [1]}
    with pytest.raises(InvalidSudokuError, match="Invalid cell id"):
        Board.from_dict(payload)


def test_from_dict_rejects_invalid_candidates() -> None:
    payload = _base_payload()
    payload["cells"] = {"a1": [0, 1]}
    with pytest.raises(InvalidSudokuError, match="Candidates for cell"):
        Board.from_dict(payload)


def test_from_dict_rejects_missing_constraint_type() -> None:
    payload = _base_payload()
    payload["constraints"] = [{}]
    with pytest.raises(InvalidSudokuError, match="must include a non-empty 'type'"):
        Board.from_dict(payload)


def test_to_dict_uses_constraints_key() -> None:
    board = Board(9)
    data = board.to_dict()
    assert "constraints" in data
    assert "constraint" not in data
    assert isinstance(data["cells"]["a1"], list)
