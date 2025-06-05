# Sudoku Solver

This project provides a simple Sudoku solver implemented in Python. The code is organised in a clean object-oriented architecture.

Run the demo with:

```bash
python main.py
```

## Project Structure

```plaintext
sudoku_solver
├─ LICENSE
├─ main.py
├─ README.md
└─ sudoku
   ├─ models
   │  ├─ board.py
   │  ├─ cell.py
   │  └─ __init__.py
   ├─ solver
   │  ├─ backtracking.py
   │  ├─ composite.py
   │  ├─ constrainst
   │  │  ├─ base_constraint.py
   │  │  ├─ clone_constraint.py
   │  │  ├─ king_constraint.py
   │  │  ├─ knight_constraint.py
   │  │  ├─ palindrome_constraint.py
   │  │  └─ __init__.py
   │  ├─ solver.py
   │  ├─ strategies
   │  │  ├─ elimination.py
   │  │  ├─ only_choice.py
   │  │  ├─ single_candidate.py
   │  │  └─ __init__.py
   │  └─ __init__.py
   ├─ utils
   │  ├─ exceptions.py
   │  ├─ io.py
   │  ├─ printer.py
   │  └─ __init__.py
   └─ __init__.py

```
