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
├─ Makefile
├─ pydoclint-baseline.txt
├─ pylint-baseline.txt
├─ pyproject.toml
├─ README.md
├─ requirements.txt
├─ ruff-baseline.txt
└─ src
   ├─ main.py
   ├─ models
   │  ├─ board.py
   │  ├─ cell.py
   │  └─ __init__.py
   ├─ solver
   │  ├─ backtracking.py
   │  ├─ composite.py
   │  ├─ constraints
   │  │  ├─ base_constraint.py
   │  │  ├─ bishop.py
   │  │  ├─ clone.py
   │  │  ├─ clone_zone_constraint.py
   │  │  ├─ even_odd.py
   │  │  ├─ killer.py
   │  │  ├─ king.py
   │  │  ├─ knight.py
   │  │  ├─ kropki.py
   │  │  ├─ palindrome.py
   │  │  ├─ universal.py
   │  │  ├─ xv.py
   │  │  └─ __init__.py
   │  ├─ solver.py
   │  ├─ strategies
   │  │  ├─ chain_violation_guard.py
   │  │  ├─ constraint.py
   │  │  ├─ elimination.py
   │  │  ├─ single_hidden.py
   │  │  ├─ subset_hidden.py
   │  │  ├─ subset_naked.py
   │  │  ├─ w_wing.py
   │  │  ├─ x_wing.py
   │  │  └─ __init__.py
   │  └─ __init__.py
   └─ utils
      ├─ exceptions.py
      ├─ gui.py
      └─ __init__.py

```
