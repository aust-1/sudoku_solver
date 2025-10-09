"""Flask API for the Sudoku solver web interface."""

from __future__ import annotations

from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS
from loggerplusplus import Logger

from models import Board
from solver import CompositeSolver
from solver.backtracking import BacktrackingSolver
from solver.strategies import (
    EliminationStrategy,
)

app = Flask(__name__, static_folder="../site", static_url_path="")
CORS(app)

logger = Logger(identifier="API", follow_logger_manager_rules=True)

# Store active board states (in production, use a proper session store)
boards: dict[str, Board] = {}
board_logs: dict[str, list[dict[str, Any]]] = {}


@app.route("/")
def index() -> Any:
    """Serve the main page."""
    return app.send_static_file("index.html")


@app.route("/api/board/new", methods=["POST"])
def create_board() -> Any:
    """Create a new board from JSON configuration.

    Request body:
        {
            "size": 9,
            "cells": {"a1": [1,2,3], ...},
            "constraint": [...]
        }

    Returns:
        {"board_id": "...", "board": {...}}
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        board = Board.from_dict(data)
        board_id = str(id(board))
        boards[board_id] = board
        board_logs[board_id] = []

        logger.info(f"Created board {board_id}")
        return jsonify({"board_id": board_id, "board": serialize_board(board)})
    except Exception as e:
        logger.error(f"Error creating board: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/board/<board_id>", methods=["GET"])
def get_board(board_id: str) -> Any:
    """Get the current state of a board."""
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    board = boards[board_id]
    return jsonify({"board": serialize_board(board)})


@app.route("/api/board/<board_id>/cell", methods=["PUT"])
def update_cell(board_id: str) -> Any:
    """Update a cell's value or candidates.

    Request body:
        {
            "pos": "a1",
            "value": 5,  // optional
            "candidates": [1,2,3]  // optional
        }
    """
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    try:
        data = request.json
        if not data or "pos" not in data:
            return jsonify({"error": "Position required"}), 400

        board = boards[board_id]
        cell = board.get_cell(pos=data["pos"])

        if "value" in data:
            cell.value = data["value"]
            board_logs[board_id].append({
                "action": "manual_set",
                "pos": data["pos"],
                "value": data["value"],
                "reason": "Manual user input",
            })

        if "candidates" in data:
            cell.candidates = set(data["candidates"])

        logger.info(f"Updated cell {data['pos']} on board {board_id}")
        return jsonify({"board": serialize_board(board)})
    except Exception as e:
        logger.error(f"Error updating cell: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/board/<board_id>/solve/step", methods=["POST"])
def solve_step(board_id: str) -> Any:
    """Execute one solving step.

    Request body:
        {
            "solver_type": "simple" | "composite" | "backtracking"
        }

    Returns:
        {
            "changed": true/false,
            "solved": true/false,
            "board": {...},
            "log": {...}
        }
    """
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    try:
        data = request.json or {}
        solver_type = data.get("solver_type", "simple")

        board = boards[board_id]
        old_state = board.to_dict()

        # Create solver based on type
        if solver_type == "simple":
            solver = EliminationStrategy()
        elif solver_type == "composite":
            solver = CompositeSolver()
        elif solver_type == "backtracking":
            solver = BacktrackingSolver()
        else:
            return jsonify({"error": f"Unknown solver type: {solver_type}"}), 400

        # Execute one step
        changed = solver.apply(board)
        solved = board.is_solved()

        # Calculate what changed
        changes = calculate_changes(old_state, board.to_dict())

        log_entry = {
            "solver": solver.__class__.__name__,
            "changed": changed,
            "changes": changes,
        }
        board_logs[board_id].append(log_entry)

        logger.info(
            f"Solved step on board {board_id} with {solver_type}: changed={changed}"
        )

        return jsonify({
            "changed": changed,
            "solved": solved,
            "board": serialize_board(board),
            "log": log_entry,
        })
    except Exception as e:
        logger.error(f"Error solving step: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/board/<board_id>/logs", methods=["GET"])
def get_logs(board_id: str) -> Any:
    """Get all logs for a board."""
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    return jsonify({"logs": board_logs.get(board_id, [])})


@app.route("/api/board/<board_id>/constraint", methods=["POST"])
def add_constraint(board_id: str) -> Any:
    """Add a constraint to a board.

    Request body:
        {
            "type": "killer",
            "cells": ["a1", "a2"],
            "sum": 15,  // constraint-specific params
            ...
        }

    Returns:
        {"board": {...}}
    """
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    try:
        from solver.constraints.factory import create_constraint_from_dict

        data = request.json
        if not data or "type" not in data:
            return jsonify({"error": "Constraint type required"}), 400

        board = boards[board_id]
        constraint = create_constraint_from_dict(board, data)
        board.add_constraints(constraint)

        logger.info(f"Added constraint {data['type']} to board {board_id}")
        return jsonify({"board": serialize_board(board)})
    except Exception as e:
        logger.error(f"Error adding constraint: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/board/<board_id>/constraint/<int:constraint_index>", methods=["DELETE"])
def delete_constraint(board_id: str, constraint_index: int) -> Any:
    """Delete a constraint from a board.

    Args:
        board_id: Board identifier
        constraint_index: Index of constraint to delete

    Returns:
        {"board": {...}}
    """
    if board_id not in boards:
        return jsonify({"error": "Board not found"}), 404

    try:
        board = boards[board_id]

        if constraint_index < 0 or constraint_index >= len(board.constraints):
            return jsonify({"error": "Invalid constraint index"}), 400

        del board.constraints[constraint_index]
        board.initialize_reachability()  # Rebuild reachability graph

        logger.info(f"Deleted constraint {constraint_index} from board {board_id}")
        return jsonify({"board": serialize_board(board)})
    except Exception as e:
        logger.error(f"Error deleting constraint: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/constraints", methods=["GET"])
def list_constraints() -> Any:
    """List all available constraint types."""
    from solver.constraints.factory import CONSTRAINT_REGISTRY

    constraints = []
    for key, cls in CONSTRAINT_REGISTRY.items():
        constraints.append({
            "id": key,
            "name": cls.__name__,
            "description": cls.__doc__ or "",
        })

    return jsonify({"constraints": constraints})


def serialize_board(board: Board) -> dict[str, Any]:
    """Serialize board to JSON-friendly format."""
    cells: list[dict[str, Any]] = []
    for cell in board.get_all_cells():
        cells.append(
            {
                "row": cell.row,
                "col": cell.col,
                "pos": cell.pos,
                "value": cell.value,
                "candidates": sorted(list(cell.candidates)),
                "is_filled": cell.is_filled(),
            },
        )

    return {
        "size": board.size,
        "cells": cells,
        "constraints": [c.to_dict() for c in board.constraints],
        "is_solved": board.is_solved(),
        "is_valid": board.is_valid(),
    }


def calculate_changes(
    old_state: dict[str, Any], new_state: dict[str, Any]
) -> list[dict[str, Any]]:
    """Calculate what changed between two board states."""
    changes = []

    old_cells = old_state["cells"]
    new_cells = new_state["cells"]

    for pos, old_candidates in old_cells.items():
        new_candidates = new_cells.get(pos, old_candidates)

        # Check if a value was set
        if len(old_candidates) > 1 and len(new_candidates) == 1:
            changes.append({
                "type": "value_set",
                "pos": pos,
                "value": new_candidates[0],
                "old_candidates": old_candidates,
            })
        # Check if candidates were eliminated
        elif set(old_candidates) != set(new_candidates):
            eliminated = set(old_candidates) - set(new_candidates)
            if eliminated:
                changes.append({
                    "type": "candidates_eliminated",
                    "pos": pos,
                    "eliminated": sorted(eliminated),
                    "remaining": sorted(new_candidates),
                })

    return changes


if __name__ == "__main__":
    app.run(debug=True, port=5000)
