"""Solving strategies for Sudoku puzzles."""

from sudoku.solver.backtracking import BacktrackingSolver
from sudoku.solver.composite import CompositeSolver
from sudoku.solver.constraints import (
    BaseConstraint,
    BishopConstraint,
    CloneConstraint,
    CloneZoneConstraint,
    KingConstraint,
    KnightConstraint,
    PalindromeConstraint,
)
from sudoku.solver.solver import Solver
from sudoku.solver.strategies import (
    ConstraintStrategy,
    EliminationStrategy,
    PairCandidateStrategy,
    PairChoiceStrategy,
    QuadCandidateStrategy,
    QuadChoiceStrategy,
    SingleCandidateStrategy,
    SingleChoiceStrategy,
    TripleCandidateStrategy,
    TripleChoiceStrategy,
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
    "KingConstraint",
    "KnightConstraint",
    "PairCandidateStrategy",
    "PairChoiceStrategy",
    "PalindromeConstraint",
    "QuadCandidateStrategy",
    "QuadChoiceStrategy",
    "SingleCandidateStrategy",
    "SingleChoiceStrategy",
    "Solver",
    "TripleCandidateStrategy",
    "TripleChoiceStrategy",
]
