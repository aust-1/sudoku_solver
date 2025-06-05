"""Solving strategies for Sudoku puzzles."""

from .constraint import ConstraintStrategy
from .elimination import EliminationStrategy
from .only_choice import OnlyChoiceStrategy
from .single_candidate import SingleCandidateStrategy

__all__ = [
    "ConstraintStrategy",
    "EliminationStrategy",
    "OnlyChoiceStrategy",
    "SingleCandidateStrategy",
]
# TODO: rajouter les autres stratégies
