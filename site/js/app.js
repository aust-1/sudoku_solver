import { getConstraint, listConstraints } from './constraints.js';

const GRID_SIZE = 9;
const state = {
    cells: Array(GRID_SIZE * GRID_SIZE).fill(null),
    constraints: Array(GRID_SIZE * GRID_SIZE).fill(null),
    selectedConstraint: 'none',
};

function init() {
    populateConstraintSelector();
    createGrid();
    document.getElementById('export-btn').addEventListener('click', exportGrid);
    document.getElementById('constraint-select').addEventListener('change', (e) => {
        state.selectedConstraint = e.target.value;
    });
}

function populateConstraintSelector() {
    const select = document.getElementById('constraint-select');
    listConstraints().forEach((constraint) => {
        const option = document.createElement('option');
        option.value = constraint.id;
        option.textContent = constraint.name;
        select.appendChild(option);
    });
}

function createGrid() {
    const grid = document.getElementById('sudoku-grid');
    for (let i = 0; i < GRID_SIZE * GRID_SIZE; i += 1) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.dataset.index = i;
        cell.addEventListener('click', handleCellClick);
        grid.appendChild(cell);
    }
}

function handleCellClick(event) {
    const index = event.target.dataset.index;
    const constraint = getConstraint(state.selectedConstraint);
    state.constraints[index] = state.selectedConstraint;
    event.target.classList.toggle('constraint-active', state.selectedConstraint !== 'none');
    // Additional logic for applying constraint graphics will go here
}

function exportGrid() {
    const data = {
        cells: state.cells,
        constraints: state.constraints,
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sudoku.json';
    a.click();
    URL.revokeObjectURL(url);
}

window.addEventListener('DOMContentLoaded', init);
