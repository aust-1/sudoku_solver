"""Solving strategies for Sudoku puzzles."""

from sudoku.solver.backtracking import BacktrackingSolver
from sudoku.solver.composite import CompositeSolver
from sudoku.solver.constraints import (
    BaseConstraint,
    BishopConstraint,
    CloneConstraint,
    CloneZoneConstraint,
    KillerConstraint,
    KingConstraint,
    KnightConstraint,
    PalindromeConstraint,
    ParityConstraint,
)
from sudoku.solver.solver import Solver
from sudoku.solver.strategies import (
    ConstraintStrategy,
    EliminationStrategy,
    HiddenPairStrategy,
    HiddenQuadStrategy,
    HiddenSingleStrategy,
    HiddenTripleStrategy,
    NakedPairStrategy,
    NakedQuadStrategy,
    NakedSingleStrategy,
    NakedTripleStrategy,
    XWingStrategy,
)

__all__ = [
    "BacktrackingSolver",
    "BaseConstraint",
    "BishopConstraint",
    "CloneConstraint",
    "CloneZoneConstraint",
    "CompositeSolver",
    "ConstraintStrategy",
    "EliminationStrategy",
    "HiddenPairStrategy",
    "HiddenQuadStrategy",
    "HiddenSingleStrategy",
    "HiddenTripleStrategy",
    "KillerConstraint",
    "KingConstraint",
    "KnightConstraint",
    "NakedPairStrategy",
    "NakedQuadStrategy",
    "NakedSingleStrategy",
    "NakedTripleStrategy",
    "PalindromeConstraint",
    "ParityConstraint",
    "Solver",
    "XWingStrategy",
]
