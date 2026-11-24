from __future__ import annotations

import pytest

from api import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def board_id(client) -> str:
    response = client.post("/api/board/new", json={"size": 9, "cells": {}})
    return response.get_json()["board_id"]


def _cell(board_json: dict, pos: str) -> dict:
    return next(cell for cell in board_json["cells"] if cell["pos"] == pos)


def _put(client, board_id: str, payload: dict):
    return client.put(f"/api/board/{board_id}/cell", json=payload)


@pytest.mark.parametrize(
    "payload",
    [
        {"pos": "z1", "value": 1},
        {"pos": "aa", "value": 1},
        {"pos": "a1", "value": "x"},
        {"pos": "a1", "value": 42},
        {"pos": "a1", "value": 0},
        {"pos": "a1", "value": True},
        {"pos": "a1", "value": None, "candidates": [1, 10]},
        {"pos": "a1", "value": None, "candidates": "123"},
    ],
)
def test_invalid_input_returns_json_400(client, board_id: str, payload: dict) -> None:
    response = _put(client, board_id, payload)
    assert response.status_code == 400  # noqa: PLR2004
    assert response.is_json
    assert response.get_json()["error"]
    a1 = _cell(client.get(f"/api/board/{board_id}").get_json()["board"], "a1")
    assert a1["value"] is None


def test_unknown_board_returns_json_404(client) -> None:
    response = client.get("/api/board/does-not-exist")
    assert response.status_code == 404  # noqa: PLR2004
    assert response.is_json
    assert response.get_json() == {"error": "Board not found"}


def test_valid_value_is_placed(client, board_id: str) -> None:
    response = _put(client, board_id, {"pos": "a1", "value": "5", "candidates": [5]})
    assert response.status_code == 200  # noqa: PLR2004
    a1 = _cell(response.get_json()["board"], "a1")
    assert a1["value"] == 5  # noqa: PLR2004


def test_clearing_a_cell_restores_candidates(client, board_id: str) -> None:
    _put(client, board_id, {"pos": "a1", "value": 5, "candidates": [5]})
    _put(client, board_id, {"pos": "a2", "value": 3, "candidates": [3]})
    response = _put(
        client, board_id, {"pos": "a2", "value": None, "candidates": list(range(1, 10))}
    )
    board = response.get_json()["board"]
    a2 = _cell(board, "a2")
    assert a2["value"] is None
    assert 5 not in a2["candidates"]  # noqa: PLR2004
    assert 3 in a2["candidates"]  # noqa: PLR2004
    for pos in ("a3", "a9", "e2", "c1"):
        assert 3 in _cell(board, pos)["candidates"]  # noqa: PLR2004
    assert 5 not in _cell(board, "a3")["candidates"]  # noqa: PLR2004

    response = client.post(
        f"/api/board/{board_id}/solve/step", json={"solver_type": "simple"}
    )
    board = response.get_json()["board"]
    a1 = _cell(board, "a1")
    assert a1["value"] == 5  # noqa: PLR2004
    assert a1["candidates"] == [5]
    assert 5 not in _cell(board, "a2")["candidates"]  # noqa: PLR2004
    assert board["is_valid"] is True


def test_replacing_a_value_gives_the_old_one_back(client, board_id: str) -> None:
    _put(client, board_id, {"pos": "a1", "value": 5, "candidates": [5]})
    response = _put(client, board_id, {"pos": "a1", "value": 6, "candidates": [6]})
    board = response.get_json()["board"]
    assert _cell(board, "a1")["value"] == 6  # noqa: PLR2004
    assert 5 in _cell(board, "a2")["candidates"]  # noqa: PLR2004
    assert 6 not in _cell(board, "a2")["candidates"]  # noqa: PLR2004


def test_clearing_respects_constraints(client, board_id: str) -> None:
    client.post(f"/api/board/{board_id}/constraint", json={"type": "king"})
    _put(client, board_id, {"pos": "c3", "value": 7})
    _put(client, board_id, {"pos": "e5", "value": 7})
    response = _put(client, board_id, {"pos": "e5", "value": None})
    board = response.get_json()["board"]
    # d4 is still a king neighbour of c3.
    assert 7 not in _cell(board, "d4")["candidates"]  # noqa: PLR2004
    assert 7 in _cell(board, "f6")["candidates"]  # noqa: PLR2004
