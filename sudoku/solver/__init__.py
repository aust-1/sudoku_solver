"""Solving strategies for Sudoku puzzles."""

from .backtracking import BacktrackingSolver
from .composite import CompositeSolver
from .constrainst import (
    CloneConstraint,
    CloneZoneConstraint,
    KingConstraint,
    KnightConstraint,
    PalindromeConstraint,
)
from .solver import Solver
from .strategies import (
    ConstraintStrategy,
    EliminationStrategy,
    PairCandidateStrategy,
    PairChoiceStrategy,
    QuadCandidateStrategy,
    QuadChoiceStrategy,
    SingleChoiceStrategy,
    SingleCandidateStrategy,
    TripleCandidateStrategy,
    TripleChoiceStrategy,
)

__all__ = [
    "BacktrackingSolver",
    "CompositeSolver",
    "CloneConstraint",
    "CloneZoneConstraint",
    "KingConstraint",
    "KnightConstraint",
    "PalindromeConstraint",
    "Solver",
    "ConstraintStrategy",
    "EliminationStrategy",
    "SingleChoiceStrategy",
    "SingleCandidateStrategy",
    "PairChoiceStrategy",
    "TripleChoiceStrategy",
    "QuadChoiceStrategy",
    "PairCandidateStrategy",
    "TripleCandidateStrategy",
    "QuadCandidateStrategy",
]
