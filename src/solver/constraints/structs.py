from enum import Enum


class ConstraintType(Enum):
    """Represents the type of constraint in the Sudoku puzzle."""

    BISHOP = "bishop"
    CLONE = "clone"
    DUTCH = "dutch"
    PARITY = "parity"
    GERMAN = "german"
    GREATER_THAN = "greater_than"
    KILLER = "killer"
    KING = "king"
    KNIGHT = "knight"
    KROPKI = "kropki"
    PALINDROME = "palindrome"
    UNIVERSAL = "universal"
    X_V = "x_v"
    UNDEFINED = "undefined"
