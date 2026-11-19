from __future__ import annotations

import pytest

from api import app
from models import Board

SOLVED = (
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


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def _cell(board_json: dict, pos: str) -> dict:
    return next(cell for cell in board_json["cells"] if cell["pos"] == pos)


def test_single_candidate_is_loaded_as_value() -> None:
    board = Board.from_dict({"size": 9, "cells": {"a1": [4]}, "constraints": []})
    a1 = board.get_cell(pos="a1")
    assert a1.value == 4  # noqa: PLR2004
    assert a1.is_filled()
    for pos in ("a2", "e1", "b2"):
        assert 4 not in board.get_cell(pos=pos).candidates  # noqa: PLR2004


def test_later_candidate_list_does_not_bring_back_a_given() -> None:
    board = Board.from_dict({
        "size": 9,
        "cells": {"a1": [4], "a2": list(range(1, 10))},
        "constraints": [],
    })
    assert 4 not in board.get_cell(pos="a2").candidates  # noqa: PLR2004


def test_given_is_propagated_through_constraints() -> None:
    board = Board.from_dict({
        "size": 9,
        "cells": {"e5": [7]},
        "constraints": [{"type": "king"}],
    })
    assert 7 not in board.get_cell(pos="f6").candidates  # noqa: PLR2004


def test_full_grid_from_json_is_solved() -> None:
    cells = {
        f"{chr(ord('a') + idx // 9)}{idx % 9 + 1}": [int(digit)]
        for idx, digit in enumerate(SOLVED)
    }
    board = Board.from_dict({"size": 9, "cells": cells, "constraints": []})
    assert board.is_solved()


def test_export_import_round_trip_keeps_values() -> None:
    board = Board(9)
    board.get_cell(pos="a1").value = 4
    board.get_cell(pos="e5").value = 7
    reloaded = Board.from_dict(board.to_dict())
    assert reloaded.get_cell(pos="a1").value == 4  # noqa: PLR2004
    assert reloaded.get_cell(pos="e5").value == 7  # noqa: PLR2004


def test_api_new_board_fills_given(client) -> None:
    response = client.post(
        "/api/board/new",
        json={"size": 9, "cells": {"a1": [4]}, "constraints": []},
    )
    board = response.get_json()["board"]
    a1 = _cell(board, "a1")
    assert a1["value"] == 4  # noqa: PLR2004
    assert a1["is_filled"] is True
    assert 4 not in _cell(board, "a2")["candidates"]  # noqa: PLR2004


def test_delete_constraint_restores_its_eliminations(client) -> None:
    board_id = client.post("/api/board/new", json={"size": 9, "cells": {}}).get_json()[
        "board_id"
    ]
    client.post(f"/api/board/{board_id}/constraint", json={"type": "knight"})
    client.post(f"/api/board/{board_id}/constraint", json={"type": "king"})
    # d4 touches c3 diagonally but shares no row, column or box with it:
    # only the king constraint removes 7 from d4.
    client.put(f"/api/board/{board_id}/cell", json={"pos": "c3", "value": 7})
    board = client.get(f"/api/board/{board_id}").get_json()["board"]
    assert 7 not in _cell(board, "d4")["candidates"]  # noqa: PLR2004

    response = client.delete(f"/api/board/{board_id}/constraint/1")
    assert response.status_code == 200  # noqa: PLR2004
    board = response.get_json()["board"]
    assert board["constraints"] == [{"type": "knight"}]
    assert 7 in _cell(board, "d4")["candidates"]  # noqa: PLR2004
    # The knight constraint is still applied.
    assert 7 not in _cell(board, "e4")["candidates"]  # noqa: PLR2004


def test_delete_constraint_keeps_placed_values(client) -> None:
    board_id = client.post("/api/board/new", json={"size": 9, "cells": {}}).get_json()[
        "board_id"
    ]
    client.post(f"/api/board/{board_id}/constraint", json={"type": "king"})
    client.put(f"/api/board/{board_id}/cell", json={"pos": "c3", "value": 3})

    response = client.delete(f"/api/board/{board_id}/constraint/0")
    board = response.get_json()["board"]
    c3 = _cell(board, "c3")
    assert c3["value"] == 3  # noqa: PLR2004
    assert c3["is_filled"] is True
    assert 3 not in _cell(board, "c4")["candidates"]  # noqa: PLR2004
    assert 3 in _cell(board, "d4")["candidates"]  # noqa: PLR2004
