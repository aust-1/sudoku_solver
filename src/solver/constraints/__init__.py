"""Model classes for Sudoku constraints."""

from solver.constraints.base_constraint import BaseConstraint
from solver.constraints.bishop import BishopConstraint
from solver.constraints.clone import CloneConstraint
from solver.constraints.clone_zone_constraint import CloneZoneConstraint
from solver.constraints.even_odd import ParityConstraint
from solver.constraints.killer import KillerConstraint
from solver.constraints.king import KingConstraint
from solver.constraints.knight import KnightConstraint
from solver.constraints.kropki import KropkiConstraint
from solver.constraints.palindrome import PalindromeConstraint
from solver.constraints.structs import ConstraintType
from solver.constraints.universal import UniversalConstraint
from solver.constraints.whispers import DutchConstraint, GermanConstraint
from solver.constraints.xv import XVConstraint

__all__ = [
    "BaseConstraint",
    "BishopConstraint",
    "CloneConstraint",
    "CloneZoneConstraint",
    "ConstraintType",
    "DutchConstraint",
    "GermanConstraint",
    "KillerConstraint",
    "KingConstraint",
    "KnightConstraint",
    "KropkiConstraint",
    "PalindromeConstraint",
    "ParityConstraint",
    "UniversalConstraint",
    "XVConstraint",
]

# TODO: Arrow
# TODO: Ascending Sequences
# TODO: Between Lines
# TODO: Consecutive
# TODO: Couples
# TODO: Diagonal
# TODO: Greater Than
# TODO: Jigsaw
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
# TODO: Windoku
# TODO: X-Sum
# TODO: Zipper Line
