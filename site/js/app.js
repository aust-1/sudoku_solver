// Main application logic for Sudoku CTC Solver Assistant
const API_BASE = `${window.location.origin}/api`;

// Application State
const state = {
  mode: "setup", // 'setup' or 'solver'
  boardId: null,
  board: null,
  initialBoard: null,
  selectedCells: [],
  selectedConstraint: null,
  constraints: [],
  stepCount: 0,
  solverCell: null, // Cell edited with the keypad in solver mode
};

const DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9];
const GRID_LABELS = {
  "sudoku-grid": "Setup grid",
  "sudoku-grid-solver": "Solver grid",
};

// Show a message in the page (announced by screen readers) instead of an alert dialog
let notificationTimer = null;
function notify(message, type = "info") {
  const area = document.getElementById("notification");
  area.className = `notification ${type}`;
  area.textContent = type === "error" ? `Error: ${message}` : message;
  clearTimeout(notificationTimer);
  notificationTimer = setTimeout(() => {
    area.textContent = "";
  }, 8000);
}

// Ask for confirmation in the page instead of a confirm dialog
async function showConfirmDialog(question, confirmLabel = "Confirm") {
  const result = await showConstraintParamModal(question, [], confirmLabel);
  return result !== null;
}

// Accessible name of a cell, e.g. "A1, empty, candidates 1 2 3"
function describeCell(cellData) {
  const pos = cellData.pos.toUpperCase();
  if (cellData.is_filled) {
    return `${pos}, value ${cellData.value}`;
  }
  if (cellData.candidates.length === 0) {
    return `${pos}, empty, no candidate`;
  }
  return `${pos}, empty, candidates ${cellData.candidates.join(" ")}`;
}

// Initialize application
document.addEventListener("DOMContentLoaded", async () => {
  await loadConstraints();
  setupEventListeners();
  createGrid("sudoku-grid");
  createGrid("sudoku-grid-solver");
  initializeBoard();
});

// Setup event listeners
function setupEventListeners() {
  // Mode switching
  document
    .getElementById("setup-mode-btn")
    .addEventListener("click", () => switchMode("setup"));
  document
    .getElementById("solver-mode-btn")
    .addEventListener("click", () => switchMode("solver"));

  // Setup mode buttons
  document
    .getElementById("add-constraint-btn")
    .addEventListener("click", addConstraint);
  document
    .getElementById("clear-board-btn")
    .addEventListener("click", clearBoard);
  document
    .getElementById("import-board-btn")
    .addEventListener("click", () =>
      document.getElementById("file-input").click()
    );
  document
    .getElementById("export-board-btn")
    .addEventListener("click", exportBoard);
  document.getElementById("file-input").addEventListener("change", importBoard);

  // Solver mode buttons
  document
    .getElementById("solve-step-btn")
    .addEventListener("click", solveStep);
  document
    .getElementById("solve-auto-btn")
    .addEventListener("click", solveAuto);
  document
    .getElementById("reset-board-btn")
    .addEventListener("click", resetBoard);

  // Keypad of the solver mode (replaces the prompt dialog)
  document.querySelectorAll(".keypad-btn").forEach((button) => {
    button.addEventListener("click", () => {
      if (!state.solverCell) return;
      const value = button.dataset.value ? parseInt(button.dataset.value) : null;
      setSolverCellValue(state.solverCell, value);
    });
  });
}

// Switch between setup and solver modes
function switchMode(mode) {
  state.mode = mode;

  // Update mode buttons
  document.querySelectorAll(".mode-btn").forEach((btn) => {
    btn.classList.remove("active");
    btn.setAttribute("aria-pressed", "false");
  });
  const modeButton = document.getElementById(`${mode}-mode-btn`);
  modeButton.classList.add("active");
  modeButton.setAttribute("aria-pressed", "true");

  // Update mode panels
  document
    .querySelectorAll(".mode-panel")
    .forEach((panel) => panel.classList.remove("active"));
  document.getElementById(`${mode}-mode`).classList.add("active");

  if (mode === "solver") {
    // Save initial board state when entering solver mode
    state.initialBoard = JSON.parse(JSON.stringify(state.board));
    renderGrid("sudoku-grid-solver");
    updateBoardStatus();
  } else if (mode === "setup") {
    // Re-render setup grid with constraints
    renderGrid("sudoku-grid");
  }
}

// Load available constraints from API
async function loadConstraints() {
  try {
    const response = await fetch(`${API_BASE}/constraints`);
    const data = await response.json();
    state.constraints = data.constraints;
    renderConstraintList();
  } catch (error) {
    console.error("Failed to load constraints:", error);
    notify("Failed to load the constraint types.", "error");
  }
}

// Render constraint list in setup mode
function renderConstraintList() {
  const list = document.getElementById("constraint-list");
  list.innerHTML = "";

  state.constraints.forEach((constraint) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "constraint-item";
    item.textContent = constraint.name.replace("Constraint", "");
    item.setAttribute("aria-pressed", "false");
    item.addEventListener("click", () => selectConstraint(constraint, item));
    list.appendChild(item);
  });
}

// Select a constraint type
function selectConstraint(constraint, itemElement) {
  state.selectedConstraint = constraint;

  // Update UI
  document.querySelectorAll(".constraint-item").forEach((item) => {
    item.classList.remove("selected");
    item.setAttribute("aria-pressed", "false");
  });
  itemElement.classList.add("selected");
  itemElement.setAttribute("aria-pressed", "true");

  // Show constraint info
  const info = document.getElementById("selected-constraint-info");
  info.innerHTML = `
        <h4>${constraint.name}</h4>
        <p>${constraint.description || "No description available."}</p>
    `;

  // Show constraint parameters (simplified for now)
  const params = document.getElementById("constraint-params");
  params.innerHTML = `
        <div class="param-group">
            <p class="param-title">Select cells on the grid</p>
            <p class="param-help">Click cells to select them for this constraint, or move with the arrow keys and press Enter or Space.</p>
        </div>
    `;

  document.getElementById("add-constraint-btn").disabled = false;
}

// Initialize board
async function initializeBoard() {
  const boardData = {
    size: 9,
    cells: {},
    constraints: [],
  };

  // Initialize all cells with candidates 1-9
  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const pos = String.fromCharCode(97 + row) + (col + 1);
      boardData.cells[pos] = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    }
  }

  try {
    const response = await fetch(`${API_BASE}/board/new`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(boardData),
    });

    const data = await response.json();
    state.boardId = data.board_id;
    state.board = data.board;
    renderGrid("sudoku-grid");
  } catch (error) {
    console.error("Failed to initialize board:", error);
    notify("Failed to create the board.", "error");
  }
}

// Create grid DOM elements (ARIA grid: rows of gridcells, roving tabindex)
function createGrid(gridId) {
  const grid = document.getElementById(gridId);
  grid.innerHTML = "";
  grid.setAttribute("role", "grid");
  grid.setAttribute("aria-label", GRID_LABELS[gridId]);
  if (gridId === "sudoku-grid") {
    grid.setAttribute("aria-multiselectable", "true");
  }

  for (let row = 0; row < 9; row++) {
    const rowElement = document.createElement("div");
    rowElement.className = "grid-row";
    rowElement.setAttribute("role", "row");

    for (let col = 0; col < 9; col++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = row;
      cell.dataset.col = col;
      cell.dataset.pos = String.fromCharCode(97 + row) + (col + 1);
      cell.setAttribute("role", "gridcell");
      cell.setAttribute("aria-label", `${cell.dataset.pos.toUpperCase()}, empty`);
      cell.tabIndex = row === 0 && col === 0 ? 0 : -1;
      if (gridId === "sudoku-grid") {
        cell.setAttribute("aria-selected", "false");
      }

      if (gridId === "sudoku-grid") {
        cell.addEventListener("click", () => handleCellClick(cell));
      } else {
        cell.addEventListener("click", () => handleSolverCellClick(cell));
      }

      rowElement.appendChild(cell);
    }
    grid.appendChild(rowElement);
  }

  grid.addEventListener("keydown", (event) => handleGridKeydown(gridId, event));
}

// Keyboard navigation in a grid: arrows, Home/End, Enter/Space, digits
function handleGridKeydown(gridId, event) {
  const cell = event.target.closest(".cell");
  if (!cell) return;
  let row = parseInt(cell.dataset.row);
  let col = parseInt(cell.dataset.col);

  switch (event.key) {
    case "ArrowUp":
      row = Math.max(0, row - 1);
      break;
    case "ArrowDown":
      row = Math.min(8, row + 1);
      break;
    case "ArrowLeft":
      col = Math.max(0, col - 1);
      break;
    case "ArrowRight":
      col = Math.min(8, col + 1);
      break;
    case "Home":
      col = 0;
      break;
    case "End":
      col = 8;
      break;
    case "Enter":
    case " ":
      event.preventDefault();
      cell.click();
      return;
    case "Delete":
    case "Backspace":
    case "0":
      if (gridId === "sudoku-grid-solver") {
        event.preventDefault();
        selectSolverCell(cell);
        setSolverCellValue(cell.dataset.pos, null);
      }
      return;
    default:
      if (gridId === "sudoku-grid-solver" && /^[1-9]$/.test(event.key)) {
        event.preventDefault();
        selectSolverCell(cell);
        setSolverCellValue(cell.dataset.pos, parseInt(event.key));
      }
      return;
  }

  event.preventDefault();
  focusCell(gridId, row, col);
}

// Move the keyboard focus (and the single tab stop) to a cell
function focusCell(gridId, row, col) {
  const grid = document.getElementById(gridId);
  const target = grid.querySelector(
    `.cell[data-row="${row}"][data-col="${col}"]`
  );
  if (!target) return;
  grid
    .querySelectorAll(".cell[tabindex='0']")
    .forEach((cell) => (cell.tabIndex = -1));
  target.tabIndex = 0;
  target.focus();
}

// Handle cell click in setup mode
function handleCellClick(cellElement) {
  const pos = cellElement.dataset.pos;

  focusCell(
    "sudoku-grid",
    parseInt(cellElement.dataset.row),
    parseInt(cellElement.dataset.col)
  );

  // Toggle selection
  if (state.selectedCells.includes(pos)) {
    state.selectedCells = state.selectedCells.filter((p) => p !== pos);
    cellElement.classList.remove("selected");
    cellElement.setAttribute("aria-selected", "false");
  } else {
    state.selectedCells.push(pos);
    cellElement.classList.add("selected");
    cellElement.setAttribute("aria-selected", "true");
  }
}

// Handle cell click in solver mode: select the cell for the keypad
function handleSolverCellClick(cellElement) {
  selectSolverCell(cellElement);
  focusCell(
    "sudoku-grid-solver",
    parseInt(cellElement.dataset.row),
    parseInt(cellElement.dataset.col)
  );
}

// Select the cell edited with the keypad (or the keyboard) in solver mode
function selectSolverCell(cellElement) {
  document
    .querySelectorAll("#sudoku-grid-solver .cell.editing")
    .forEach((cell) => cell.classList.remove("editing"));
  cellElement.classList.add("editing");
  state.solverCell = cellElement.dataset.pos;

  document.getElementById(
    "cell-editor-target"
  ).textContent = `Selected cell: ${state.solverCell.toUpperCase()}. Type a digit or use the buttons below.`;
  document
    .querySelectorAll(".keypad-btn")
    .forEach((button) => (button.disabled = false));
}

// Set (or clear, with null) the value of a cell in solver mode
function setSolverCellValue(pos, value) {
  if (value === null) {
    // Clear cell - reset to all candidates
    updateCell(pos, null, [...DIGITS]);
  } else {
    updateCell(pos, value, [value]);
  }
}

// Update cell value
async function updateCell(pos, value, candidates) {
  try {
    const response = await fetch(`${API_BASE}/board/${state.boardId}/cell`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pos, value, candidates }),
    });

    const data = await response.json();
    if (!response.ok || data.error) {
      notify(data.error || "Failed to update the cell.", "error");
      return;
    }
    state.board = data.board;
    renderGrid("sudoku-grid-solver");
    updateBoardStatus();
    notify(
      value === null
        ? `${pos.toUpperCase()} cleared.`
        : `${pos.toUpperCase()} set to ${value}.`
    );
  } catch (error) {
    console.error("Failed to update cell:", error);
    notify("Failed to update the cell.", "error");
  }
}

// Add constraint to board
async function addConstraint() {
  if (!state.selectedConstraint) {
    notify("Please select a constraint type.", "error");
    return;
  }

  // Global constraints don't require cell selection
  const globalConstraints = ["knight", "king", "universal"];
  if (
    !globalConstraints.includes(state.selectedConstraint.id) &&
    state.selectedCells.length === 0
  ) {
    notify("Please select at least one cell.", "error");
    return;
  }

  const constraintData = {
    type: state.selectedConstraint.id,
    cells: state.selectedCells,
  };

  // Add constraint-specific parameters based on type
  let params = null;

  if (state.selectedConstraint.id === "killer") {
    params = await showConstraintParamModal("Killer Cage Sum: ", [
      { name: "sum", label: "Sum", type: "number", required: true },
    ]);
    if (!params) return;
    constraintData.sum = parseInt(params.sum);
  } else if (state.selectedConstraint.id === "kropki") {
    if (state.selectedCells.length !== 2) {
      notify("Kropki constraint requires exactly 2 adjacent cells.", "error");
      return;
    }
    params = await showConstraintParamModal("Kropki Dot Type: ", [
      {
        name: "color",
        label: "Dot Type",
        type: "select",
        options: [
          { value: "black", label: "Black (ratio 2:1)" },
          { value: "white", label: "White (consecutive)" },
        ],
        required: true,
      },
    ]);
    if (!params) return;
    constraintData.cell1 = state.selectedCells[0];
    constraintData.cell2 = state.selectedCells[1];
    constraintData.color = params.color;
    delete constraintData.cells;
  } else if (state.selectedConstraint.id === "xv") {
    if (state.selectedCells.length !== 2) {
      notify("XV constraint requires exactly 2 adjacent cells.", "error");
      return;
    }
    params = await showConstraintParamModal("XV Constraint Type: ", [
      {
        name: "type",
        label: "Type",
        type: "select",
        options: [
          { value: "10", label: "X (sum = 10)" },
          { value: "5", label: "V (sum = 5)" },
        ],
        required: true,
      },
    ]);
    if (!params) return;
    constraintData.cell1 = state.selectedCells[0];
    constraintData.cell2 = state.selectedCells[1];
    constraintData.sum = parseInt(params.type);
    delete constraintData.cells;
  } else if (state.selectedConstraint.id === "parity") {
    if (state.selectedCells.length !== 1) {
      notify("Parity constraint requires exactly 1 cell.", "error");
      return;
    }
    params = await showConstraintParamModal("Parity Type: ", [
      {
        name: "rest",
        label: "Type",
        type: "select",
        options: [
          { value: "1", label: "Odd" },
          { value: "0", label: "Even" },
        ],
        required: true,
      },
    ]);
    if (!params) return;
    constraintData.cell = state.selectedCells[0];
    constraintData.rest = parseInt(params.rest);
    delete constraintData.cells;
  } else if (state.selectedConstraint.id === "greater_than") {
    if (state.selectedCells.length !== 2) {
      notify("GreaterThan constraint requires exactly 2 adjacent cells.", "error");
      return;
    }
    constraintData.higher_value_cell = state.selectedCells[0];
    constraintData.lower_value_cell = state.selectedCells[1];
    delete constraintData.cells;
  } else if (
    state.selectedConstraint.id === "knight" ||
    state.selectedConstraint.id === "king" ||
    state.selectedConstraint.id === "universal"
  ) {
    // These constraints don't require cell selection
    delete constraintData.cells;
  }

  try {
    const response = await fetch(
      `${API_BASE}/board/${state.boardId}/constraint`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(constraintData),
      }
    );

    const data = await response.json();

    if (data.error) {
      notify(data.error, "error");
      return;
    }

    state.board = data.board;
    renderGrid("sudoku-grid");
    renderConstraints("sudoku-grid", state.board.constraints);
    updateActiveConstraints();

    // Clear selection
    state.selectedCells = [];
    document.querySelectorAll(".cell.selected").forEach((cell) => {
      cell.classList.remove("selected");
      cell.setAttribute("aria-selected", "false");
    });

    notify(`Constraint "${state.selectedConstraint.name}" added.`);
  } catch (error) {
    console.error("Failed to add constraint:", error);
    notify("Failed to add constraint.", "error");
  }
}

// Update active constraints display
function updateActiveConstraints() {
  const list = document.getElementById("constraint-list-display");
  list.innerHTML = "";

  if (!state.board || !state.board.constraints) return;

  state.board.constraints.forEach((constraint, index) => {
    const item = document.createElement("li");
    const label = document.createElement("span");
    label.textContent = constraint.type;
    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "constraint-delete";
    deleteBtn.textContent = "✕";
    deleteBtn.setAttribute(
      "aria-label",
      `Delete constraint ${index + 1} (${constraint.type})`
    );
    deleteBtn.addEventListener("click", () => deleteConstraint(index));
    item.append(label, deleteBtn);

    list.appendChild(item);
  });
}

// Delete constraint
async function deleteConstraint(index) {
  if (!(await showConfirmDialog("Delete this constraint?", "Delete"))) return;

  try {
    const response = await fetch(
      `${API_BASE}/board/${state.boardId}/constraint/${index}`,
      {
        method: "DELETE",
      }
    );

    const data = await response.json();

    if (data.error) {
      notify(data.error, "error");
      return;
    }

    state.board = data.board;
    renderGrid("sudoku-grid");
    updateActiveConstraints();
    notify("Constraint deleted.");
  } catch (error) {
    console.error("Failed to delete constraint:", error);
    notify("Failed to delete constraint.", "error");
  }
}

// Render grid with current board state
function renderGrid(gridId) {
  if (!state.board) return;

  const grid = document.getElementById(gridId);
  const cells = grid.querySelectorAll(".cell");

  state.board.cells.forEach((cellData, index) => {
    const cellElement = cells[index];
    cellElement.innerHTML = "";
    cellElement.classList.remove("changed", "eliminated");
    cellElement.setAttribute("aria-label", describeCell(cellData));

    if (cellData.is_filled) {
      // Show value
      const valueDiv = document.createElement("div");
      valueDiv.className = "cell-value";
      valueDiv.textContent = cellData.value;
      cellElement.appendChild(valueDiv);
    } else {
      // Show candidates
      const candidatesDiv = document.createElement("div");
      candidatesDiv.className = "cell-candidates";
      // The cell label already lists the candidates
      candidatesDiv.setAttribute("aria-hidden", "true");

      for (let i = 1; i <= 9; i++) {
        const candidate = document.createElement("div");
        candidate.className = "candidate";
        if (cellData.candidates.includes(i)) {
          candidate.textContent = i;
        }
        candidatesDiv.appendChild(candidate);
      }

      cellElement.appendChild(candidatesDiv);
    }
  });

  // Render constraints if they exist
  if (state.board.constraints && state.board.constraints.length > 0) {
    renderConstraints(gridId, state.board.constraints);
  }
}

// Solve one step
async function solveStep() {
  const solverType = document.getElementById("solver-type").value;

  try {
    const response = await fetch(
      `${API_BASE}/board/${state.boardId}/solve/step`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ solver_type: solverType }),
      }
    );

    const data = await response.json();

    if (data.error) {
      notify(data.error, "error");
      return;
    }

    state.board = data.board;
    state.stepCount++;

    // Highlight changed cells
    highlightChanges(data.log.changes);

    // Add log entry
    addLogEntry(data.log, data.changed, data.solved);

    // Update grid and status
    renderGrid("sudoku-grid-solver");
    updateBoardStatus();

    if (data.solved) {
      notify("🎉 Puzzle solved!", "success");
    } else if (!data.changed) {
      notify("No progress made. Try a different solver or manual intervention.");
    } else {
      notify(`Step ${state.stepCount}: ${summarizeChanges(data.log.changes)}.`);
    }
  } catch (error) {
    console.error("Failed to solve step:", error);
    notify("Failed to execute solving step.", "error");
  }
}

// Auto solve
async function solveAuto() {
  const solverType = document.getElementById("solver-type").value;
  let maxSteps = 100;

  while (maxSteps-- > 0) {
    const response = await fetch(
      `${API_BASE}/board/${state.boardId}/solve/step`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ solver_type: solverType }),
      }
    );

    const data = await response.json();

    if (data.error) {
      notify(data.error, "error");
      break;
    }

    state.board = data.board;
    state.stepCount++;

    addLogEntry(data.log, data.changed, data.solved);
    renderGrid("sudoku-grid-solver");
    updateBoardStatus();

    if (data.solved) {
      notify("🎉 Puzzle solved!", "success");
      break;
    }

    if (!data.changed) {
      notify("Cannot make further progress automatically.");
      break;
    }

    // Small delay for visualization
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
}

// Short text summary of the changes of a step
function summarizeChanges(changes) {
  const values = changes.filter((c) => c.type === "value_set").length;
  const eliminations = changes.length - values;
  return `${values} value(s) set, candidates eliminated in ${eliminations} cell(s)`;
}

// Highlight changed cells
function highlightChanges(changes) {
  if (!changes) return;

  changes.forEach((change) => {
    const cell = document.querySelector(
      `#sudoku-grid-solver .cell[data-pos="${change.pos}"]`
    );
    if (cell) {
      if (change.type === "value_set") {
        cell.classList.add("changed");
      } else if (change.type === "candidates_eliminated") {
        cell.classList.add("eliminated");
      }

      setTimeout(() => {
        cell.classList.remove("changed", "eliminated");
      }, 1000);
    }
  });
}

// Add log entry
function addLogEntry(log, changed, solved) {
  const container = document.getElementById("log-container");

  const entry = document.createElement("div");
  entry.className = `log-entry ${
    solved ? "success" : changed ? "" : "no-change"
  }`;

  let changesHtml = "";
  if (log.changes && log.changes.length > 0) {
    changesHtml = '<div class="log-changes">';
    log.changes.forEach((change) => {
      if (change.type === "value_set") {
        changesHtml += `<div class="change-item value-set">✓ ${change.pos.toUpperCase()}: Set value ${
          change.value
        }</div>`;
      } else if (change.type === "candidates_eliminated") {
        changesHtml += `<div class="change-item candidates-eliminated">✗ ${change.pos.toUpperCase()}: Eliminated ${change.eliminated.join(
          ", "
        )}</div>`;
      }
    });
    changesHtml += "</div>";
  } else {
    changesHtml = '<div class="log-changes"><em>No changes</em></div>';
  }

  entry.innerHTML = `
        <div class="log-header">Step ${state.stepCount}: ${log.solver}</div>
        ${changesHtml}
    `;

  container.insertBefore(entry, container.firstChild);
}

// Update board status
function updateBoardStatus() {
  if (!state.board) return;

  document.getElementById("status-valid").textContent = state.board.is_valid
    ? "✓ Yes"
    : "✗ No";
  document.getElementById("status-solved").textContent = state.board.is_solved
    ? "✓ Yes"
    : "✗ No";
  document.getElementById("status-steps").textContent = state.stepCount;
}

// Reset board to initial state
function resetBoard() {
  if (!state.initialBoard) return;

  state.board = JSON.parse(JSON.stringify(state.initialBoard));
  state.stepCount = 0;
  renderGrid("sudoku-grid-solver");
  updateBoardStatus();
  document.getElementById("log-container").innerHTML = "";
}

// Clear board
async function clearBoard() {
  if (await showConfirmDialog("Clear the entire board?", "Clear")) {
    initializeBoard();
    state.selectedCells = [];
    document
      .querySelectorAll(".cell.selected")
      .forEach((cell) => cell.classList.remove("selected"));
  }
}

// Export board
function exportBoard() {
  if (!state.board) return;

  const data = {
    size: state.board.size,
    cells: {},
    constraints: state.board.constraints,
  };

  // Convert cells array to dictionary format
  state.board.cells.forEach((cell) => {
    data.cells[cell.pos] = cell.candidates;
  });

  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "sudoku-board.json";
  a.click();
  URL.revokeObjectURL(url);
}

// Show modal for constraint parameters (accessible dialog: focus moved into
// the dialog and kept there, Escape cancels, focus restored on close)
function showConstraintParamModal(title, fields, okLabel = "OK") {
  return new Promise((resolve) => {
    const modal = document.getElementById("constraint-param-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");
    const okBtn = document.getElementById("modal-ok");
    const cancelBtn = document.getElementById("modal-cancel");
    const previouslyFocused = document.activeElement;

    modalTitle.textContent = title;
    okBtn.textContent = okLabel;
    modalBody.innerHTML = "";

    // Create form fields, each label tied to its field
    fields.forEach((field) => {
      const label = document.createElement("label");
      label.textContent = field.label;
      label.htmlFor = `modal-${field.name}`;
      modalBody.appendChild(label);

      let input;
      if (field.type === "select") {
        input = document.createElement("select");
        input.id = `modal-${field.name}`;
        field.options.forEach((option) => {
          const opt = document.createElement("option");
          opt.value = option.value;
          opt.textContent = option.label;
          input.appendChild(opt);
        });
      } else {
        input = document.createElement("input");
        input.type = field.type;
        input.id = `modal-${field.name}`;
        if (field.required) input.required = true;
      }
      modalBody.appendChild(input);
    });

    modal.classList.add("active");
    modal.setAttribute("aria-hidden", "false");
    const firstField = modalBody.querySelector("input, select");
    (firstField || okBtn).focus();

    const cleanup = () => {
      modal.classList.remove("active");
      modal.setAttribute("aria-hidden", "true");
      okBtn.removeEventListener("click", handleOk);
      cancelBtn.removeEventListener("click", handleCancel);
      modal.removeEventListener("keydown", handleKeydown);
      if (previouslyFocused && previouslyFocused.focus) {
        previouslyFocused.focus();
      }
    };

    const handleOk = () => {
      const result = {};
      fields.forEach((field) => {
        const input = document.getElementById(`modal-${field.name}`);
        result[field.name] = input.value;
      });
      cleanup();
      resolve(result);
    };

    const handleCancel = () => {
      cleanup();
      resolve(null);
    };

    const handleKeydown = (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        handleCancel();
      } else if (event.key === "Tab") {
        // Keep the focus inside the dialog
        const focusable = [
          ...modal.querySelectorAll("input, select, button"),
        ].filter((element) => !element.disabled);
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    };

    okBtn.addEventListener("click", handleOk);
    cancelBtn.addEventListener("click", handleCancel);
    modal.addEventListener("keydown", handleKeydown);
  });
}

// Import board
async function importBoard(event) {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const text = await file.text();
    const data = JSON.parse(text);

    const response = await fetch(`${API_BASE}/board/new`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    state.boardId = result.board_id;
    state.board = result.board;
    renderGrid("sudoku-grid");
    renderConstraints("sudoku-grid", state.board.constraints);
    updateActiveConstraints();

    notify("Board imported successfully!", "success");
  } catch (error) {
    console.error("Failed to import board:", error);
    notify("Failed to import board. Please check the file format.", "error");
  }
}
