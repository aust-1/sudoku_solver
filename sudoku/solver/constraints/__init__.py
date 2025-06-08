"""Model classes for Sudoku constraints."""

from sudoku.solver.constraints.base_constraint import BaseConstraint
from sudoku.solver.constraints.bishop import BishopConstraint
from sudoku.solver.constraints.clone import CloneConstraint
from sudoku.solver.constraints.clone_zone_constraint import CloneZoneConstraint
from sudoku.solver.constraints.king import KingConstraint
from sudoku.solver.constraints.knight import KnightConstraint
from sudoku.solver.constraints.palindrome import PalindromeConstraint

__all__ = [
    "BaseConstraint",
    "BishopConstraint",
    "CloneConstraint",
    "CloneZoneConstraint",
    "KingConstraint",
    "KnightConstraint",
    "PalindromeConstraint",
]

# TODO: Arrow
# TODO: Ascending Sequences
# TODO: Between Lines
# TODO: Consecutive
# TODO: Couples
# TODO: Diagonal
# TODO: Dutch
# TODO: Even-Odd
# TODO: German
# TODO: Greater Than
# TODO: Jigsaw
# TODO: Killer
# TODO: Kropki
# TODO: Little Unique Killer
# TODO: Lockout Lines
# TODO: Non-Consecutive
# TODO: Quadruple
# TODO: Reflection
# TODO: Renban
# TODO: Running Cells
# TODO: Sandwich
# TODO: Skyscraper
# TODO: Slingshot
# TODO: Slow Thermo
# TODO: Thermo
# TODO: Twisted Consecutive
# TODO: Universal
# TODO: Windoku
# TODO: X-Sum
# TODO: XV
# TODO: Zipper Line
