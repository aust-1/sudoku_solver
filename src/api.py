"""Flask API for the Sudoku solver web interface."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, Response, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from models import Board
from solver import CompositeSolver
from solver.backtracking import BacktrackingSolver
from solver.constraints.factory import CONSTRAINT_REGISTRY, create_constraint_from_dict
from solver.strategies import EliminationStrategy
from utils.exceptions import InvalidSudokuError

ROOT_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT_DIR / "site"

app = Flask(__name__)
CORS(app)

boards: dict[str, Board] = {}
board_constraints: dict[str, list[dict[str, Any]]] = {}
board_logs: dict[str, list[dict[str, Any]]] = {}
current_board: Board | None = None
current_constraints: list[dict[str, Any]] = []


def set_current_board_for_tests(board: Board) -> None:
    global current_board, current_constraints
    current_board = board
    current_constraints = [c.to_dict() for c in board.constraints]


def _default_board_payload(size: int = 9) -> dict[str, Any]:
    cells: dict[str, list[int]] = {}
    for row in range(size):
        for col in range(size):
            pos = f"{chr(97 + row)}{col + 1}"
            cells[pos] = list(range(1, size + 1))
    return {"size": size, "cells": cells, "constraints": []}


def _alias_constraint_type(constraint_type: str) -> str:
    if constraint_type == "xv":
        return "x_v"
    return constraint_type


def _normalize_board_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return _default_board_payload()

    normalized = dict(payload)
    if "constraints" not in normalized and "constraint" in normalized:
        normalized["constraints"] = normalized.pop("constraint")

    if "size" not in normalized or "cells" not in normalized:
        size = int(normalized.get("size", 9))
        base = _default_board_payload(size)
        base.update(normalized)
        normalized = base

    constraints = normalized.get("constraints", [])
    if isinstance(constraints, list):
        normalized_constraints = []
        for constraint in constraints:
            if not isinstance(constraint, dict):
                normalized_constraints.append(constraint)
                continue
            normalized_constraint = dict(constraint)
            constraint_type = normalized_constraint.get("type")
            if isinstance(constraint_type, str):
                normalized_constraint["type"] = _alias_constraint_type(constraint_type)
            normalized_constraints.append(normalized_constraint)
        normalized["constraints"] = normalized_constraints

    return normalized


def _serialize_board_ui(
    board: Board, constraints: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "size": board.size,
        "cells": [
            {
                "row": cell.row,
                "col": cell.col,
                "pos": cell.pos,
                "value": cell.value,
                "candidates": sorted(cell.candidates),
                "is_filled": cell.is_filled(),
            }
            for cell in board.get_all_cells()
        ],
        "constraints": constraints,
        "is_valid": board.is_valid(),
        "is_solved": board.is_solved(),
    }


def _serialize_board_export(
    board: Board, constraints: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "size": board.size,
        "cells": {cell.pos: sorted(cell.candidates) for cell in board.get_all_cells()},
        "constraints": constraints,
    }


def _snapshot_board(board: Board) -> dict[str, dict[str, Any]]:
    snapshot: dict[str, dict[str, Any]] = {}
    for cell in board.get_all_cells():
        snapshot[cell.pos] = {
            "value": cell.value,
            "candidates": set(cell.candidates),
        }
    return snapshot


def _diff_snapshots(
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    for pos, before_state in before.items():
        after_state = after[pos]
        before_value = before_state["value"]
        after_value = after_state["value"]
        if before_value != after_value and after_value is not None:
            changes.append({
                "type": "value_set",
                "pos": pos,
                "value": after_value,
            })
            continue

        before_candidates = before_state["candidates"]
        after_candidates = after_state["candidates"]
        eliminated = sorted(before_candidates - after_candidates)
        if eliminated:
            changes.append({
                "type": "candidates_eliminated",
                "pos": pos,
                "eliminated": eliminated,
                "remaining": sorted(after_candidates),
            })

    return changes


def _create_board(payload: dict[str, Any]) -> tuple[Board, list[dict[str, Any]]]:
    raw_constraints = payload.get("constraints", payload.get("constraint", []))
    constraints_list: list[dict[str, Any]] = []
    if isinstance(raw_constraints, list):
        for constraint in raw_constraints:
            if isinstance(constraint, dict):
                constraints_list.append(constraint)

    normalized = _normalize_board_payload(payload)
    board = Board.from_dict(normalized)
    return board, constraints_list


def _build_constraint_catalog() -> list[dict[str, str]]:
    catalog: list[dict[str, str]] = []
    for constraint_type in sorted(CONSTRAINT_REGISTRY.keys()):
        display_type = "xv" if constraint_type == "x_v" else constraint_type
        if display_type == "xv":
            name = "XVConstraint"
        else:
            parts = display_type.split("_")
            name = "".join(part.capitalize() for part in parts) + "Constraint"
        catalog.append({
            "id": display_type,
            "name": name,
            "description": f"{display_type.replace('_', ' ').title()} constraint.",
        })
    return catalog


def _get_board_or_404(board_id: str) -> Board:
    board = boards.get(board_id)
    if board is None:
        abort(404, description="Board not found")
    return board


@app.errorhandler(HTTPException)
def handle_http_error(error: HTTPException) -> tuple[Response, int] | HTTPException:
    """Return API errors as JSON instead of Flask's HTML pages.

    Unhandled exceptions reach this handler as a 500 ``InternalServerError``.

    Args:
        error (HTTPException): The HTTP error raised while handling the request.

    Returns:
        tuple[Response, int] | HTTPException:
            A JSON response for ``/api`` routes, the default page otherwise.
    """
    if not request.path.startswith("/api/"):
        return error
    return jsonify({"error": error.description}), error.code or 500


def _parse_digit(raw: object, size: int, field: str) -> int:
    """Convert ``raw`` to a digit between 1 and ``size``.

    Args:
        raw (object): The value read from the JSON payload.
        size (int): The size of the board.
        field (str): The name of the field, used in the error message.

    Returns:
        int: The digit.

    Raises:
        ValueError: If ``raw`` is not an integer between 1 and ``size``.
    """
    digit: int | None = None
    if isinstance(raw, int) and not isinstance(raw, bool):
        digit = raw
    elif isinstance(raw, str) and raw.strip().isdigit():
        digit = int(raw.strip())
    if digit is None or not 1 <= digit <= size:
        msg = f"{field} must be an integer between 1 and {size}, got {raw!r}."
        raise ValueError(msg)
    return digit


def _apply_constraint(board: Board, constraint_data: dict[str, Any]) -> None:
    normalized = dict(constraint_data)
    constraint_type = normalized.get("type")
    if isinstance(constraint_type, str):
        normalized["type"] = _alias_constraint_type(constraint_type)
    constraint = create_constraint_from_dict(board, normalized)
    board.add_constraints(constraint)


def _solver_for_type(solver_type: str):
    if solver_type == "simple":
        return EliminationStrategy()
    if solver_type == "backtracking":
        return BacktrackingSolver()
    return CompositeSolver()


@app.route("/")
def index() -> Any:
    return send_from_directory(SITE_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename: str) -> Any:
    if filename.startswith("api"):
        abort(404)
    return send_from_directory(SITE_DIR, filename)


@app.get("/api/constraints")
def get_constraints() -> Any:
    return jsonify({"constraints": _build_constraint_catalog()})


@app.post("/api/board/new")
def create_board() -> Any:
    payload = request.get_json(silent=True)
    try:
        board, constraints_list = _create_board(payload or {})
    except (InvalidSudokuError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    board_id = str(uuid.uuid4())
    boards[board_id] = board
    board_constraints[board_id] = constraints_list
    board_logs[board_id] = []

    global current_board, current_constraints
    current_board = board
    current_constraints = constraints_list

    return jsonify({
        "board_id": board_id,
        "board": _serialize_board_ui(board, constraints_list),
    })


@app.get("/api/board/<board_id>")
def get_board(board_id: str) -> Any:
    board = _get_board_or_404(board_id)
    return jsonify({
        "board": _serialize_board_ui(board, board_constraints.get(board_id, [])),
    })


@app.put("/api/board/<board_id>/cell")
def update_cell(board_id: str) -> Any:
    board = _get_board_or_404(board_id)
    payload = request.get_json(silent=True) or {}
    pos = payload.get("pos")
    if not isinstance(pos, str):
        return jsonify({"error": "Missing cell position."}), 400

    try:
        cell = board.get_cell(pos=pos)
    except ValueError:
        return jsonify({"error": f"Invalid cell position: {pos}."}), 400

    raw_value = payload.get("value")
    raw_candidates = payload.get("candidates")
    try:
        value = (
            None if raw_value is None else _parse_digit(raw_value, board.size, "value")
        )
        candidates: set[int] | None = None
        if raw_candidates is not None:
            if not isinstance(raw_candidates, list):
                return jsonify({"error": "Candidates must be a list."}), 400
            candidates = {
                _parse_digit(c, board.size, "candidates") for c in raw_candidates
            }
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if cell.is_filled() and cell.value != value:
        # The old value was removed from the reachable cells: give it back.
        board.clear_cell(cell)
        if value is None and candidates is not None:
            cell.candidates &= candidates
    elif value is None and candidates is not None:
        cell.candidates = candidates

    if value is not None:
        cell.value = value

    return jsonify({
        "board": _serialize_board_ui(board, board_constraints.get(board_id, [])),
    })


@app.post("/api/board/<board_id>/constraint")
def add_constraint(board_id: str) -> Any:
    board = _get_board_or_404(board_id)
    payload = request.get_json(silent=True) or {}
    if "type" not in payload:
        return jsonify({"error": "Missing constraint type."}), 400

    try:
        _apply_constraint(board, payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    constraints_list = board_constraints.setdefault(board_id, [])
    constraints_list.append(payload)

    return jsonify({
        "board": _serialize_board_ui(board, constraints_list),
    })


@app.delete("/api/board/<board_id>/constraint/<int:index>")
def delete_constraint(board_id: str, index: int) -> Any:
    board = _get_board_or_404(board_id)
    constraints_list = board_constraints.get(board_id, [])
    if index < 0 or index >= len(constraints_list):
        return jsonify({"error": "Constraint index out of range."}), 400

    new_constraints = [
        constraint for idx, constraint in enumerate(constraints_list) if idx != index
    ]
    board_data = _serialize_board_export(board, new_constraints)
    board, _ = _create_board(board_data)

    boards[board_id] = board
    board_constraints[board_id] = new_constraints

    return jsonify({
        "board": _serialize_board_ui(board, new_constraints),
    })


@app.post("/api/board/<board_id>/solve/step")
def solve_step(board_id: str) -> Any:
    board = _get_board_or_404(board_id)
    payload = request.get_json(silent=True) or {}
    solver_type = payload.get("solver_type", "composite")
    if not isinstance(solver_type, str):
        solver_type = "composite"

    solver = _solver_for_type(solver_type)
    before = _snapshot_board(board)
    solver.apply(board)
    after = _snapshot_board(board)

    changes = _diff_snapshots(before, after)
    changed = len(changes) > 0
    solved = board.is_solved()

    log_entry = {
        "action": "solve_step",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "solver": solver.__class__.__name__,
        "changed": changed,
        "changes": changes,
    }
    board_logs.setdefault(board_id, []).append(log_entry)

    return jsonify({
        "changed": changed,
        "solved": solved,
        "board": _serialize_board_ui(board, board_constraints.get(board_id, [])),
        "log": log_entry,
    })


@app.get("/api/board/<board_id>/logs")
def get_logs(board_id: str) -> Any:
    _get_board_or_404(board_id)
    return jsonify({"logs": board_logs.get(board_id, [])})


@app.get("/api/board")
def export_board() -> Any:
    if current_board is None:
        return jsonify(_default_board_payload())
    return jsonify(_serialize_board_export(current_board, current_constraints))


@app.post("/api/board/import")
def import_board() -> Any:
    payload = request.get_json(silent=True) or {}
    try:
        board, constraints_list = _create_board(payload)
    except (InvalidSudokuError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    global current_board, current_constraints
    current_board = board
    current_constraints = constraints_list

    return jsonify({
        "board": _serialize_board_export(board, constraints_list),
        "delta": {
            "cells": payload.get("cells", {}),
            "constraints": payload.get("constraints", payload.get("constraint", [])),
        },
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
