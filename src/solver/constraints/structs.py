from enum import Enum


class ConstraintType(Enum):
    """Represents the type of constraint in the Sudoku puzzle."""

    AXIA = "axia"
    BISHOP = "bishop"
    CLONE = "clone"
    COUPLE = "couple"
    DUTCH = "dutch"
    FRIENDLY_CELL = "friendly_cell"
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
