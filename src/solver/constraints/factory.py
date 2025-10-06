from __future__ import annotations

from typing import TYPE_CHECKING, Any

from solver.constraints import (
    BishopConstraint,
    CloneConstraint,
    CloneZoneConstraint,
    DutchConstraint,
    GermanConstraint,
    GreaterThanConstraint,
    KillerConstraint,
    KingConstraint,
    KnightConstraint,
    KropkiConstraint,
    PalindromeConstraint,
    ParityConstraint,
    UniversalConstraint,
    XVConstraint,
)

if TYPE_CHECKING:
    from models import Board
    from solver.constraints import BaseConstraint

CONSTRAINT_REGISTRY: dict[str, type[BaseConstraint]] = {
    "bishop": BishopConstraint,
    "clone": CloneConstraint,
    "clone_zone": CloneZoneConstraint,
    "dutch": DutchConstraint,
    "german": GermanConstraint,
    "greater_than": GreaterThanConstraint,
    "killer": KillerConstraint,
    "king": KingConstraint,
    "knight": KnightConstraint,
    "kropki": KropkiConstraint,
    "palindrome": PalindromeConstraint,
    "parity": ParityConstraint,
    "universal": UniversalConstraint,
    "x_v": XVConstraint,
}


def get_constraint_class(constraint_type: str) -> type[BaseConstraint] | None:
    """Get constraint class by type name.

    Args:
        constraint_type (str): The constraint type identifier.

    Returns:
        type[BaseConstraint] | None:
            The constraint class or None if not found.
    """
    return CONSTRAINT_REGISTRY.get(constraint_type.lower())


def create_constraint_from_dict(board: Board, data: dict[str, Any]) -> BaseConstraint:
    """Create a constraint instance from dictionary data.

    Args:
        board (Board): The Sudoku board the constraint applies to.
        data (dict[str, Any]): Dictionary containing constraint configuration.
            Must include a 'type' field.

    Returns:
        BaseConstraint: The created constraint instance.

    Raises:
        ValueError: If constraint type is unknown or data is invalid.
    """
    if "type" not in data:
        msg = "Constraint data must include 'type' field"
        raise ValueError(msg)

    constraint_type = data["type"]
    constraint_class = get_constraint_class(constraint_type)

    if constraint_class is None:
        msg = f"Unknown constraint type: {constraint_type}"
        raise ValueError(msg)

    return constraint_class.from_dict(board, data)
