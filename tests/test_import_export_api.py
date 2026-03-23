from __future__ import annotations

import json

import pytest

from api import app, set_current_board_for_tests
from models import Board


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def _sorted_constraints(constraints: list[dict[str, object]]) -> list[str]:
    return sorted(json.dumps(c, sort_keys=True) for c in constraints)


def test_get_board_returns_boardfile(flask_client) -> None:
    board = Board(9)
    set_current_board_for_tests(board)

    response = flask_client.get("/api/board")
    assert response.status_code == 200
    data = response.get_json()

    assert set(data.keys()) == {"size", "cells", "constraints"}
    assert data["size"] == 9
    assert "a1" in data["cells"]


def test_import_export_round_trip(client) -> None:
    payload = {
        "size": 9,
        "cells": {"a1": [1], "a2": [1, 2], "b1": [3]},
        "constraints": [
            {"type": "knight"},
            {"type": "palindrome", "cells": ["a1", "a2"]},
        ],
    }

    response = client.post("/api/board/import", json=payload)
    assert response.status_code == 200
    body = response.get_json()

    board = body["board"]
    delta = body["delta"]

    for cell_id, candidates in payload["cells"].items():
        assert board["cells"][cell_id] == candidates

    assert _sorted_constraints(board["constraints"]) == _sorted_constraints(
        payload["constraints"],
    )

    assert delta["cells"]["a1"] == [1]
    assert _sorted_constraints(delta["constraints"]) == _sorted_constraints(
        payload["constraints"],
    )

    response = client.get("/api/board")
    assert response.status_code == 200
    exported = response.get_json()
    assert exported["cells"]["a2"] == [1, 2]
    assert _sorted_constraints(exported["constraints"]) == _sorted_constraints(
        payload["constraints"],
    )
