"""Solving strategies for Sudoku puzzles."""

from .constraint import ConstraintStrategy
from .elimination import EliminationStrategy
from .single_choice import SingleChoiceStrategy
from .single_candidate import SingleCandidateStrategy

__all__ = [
    "ConstraintStrategy",
    "EliminationStrategy",
    "SingleChoiceStrategy",
    "SingleCandidateStrategy",
]
# TODO: rajouter les autres stratégies
