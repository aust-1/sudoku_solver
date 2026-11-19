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
  autoSolving: false,
};

// Error raised when the API cannot be reached or answers with an error
class ApiError extends Error {
  constructor(message, status = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

// Call the API and return the JSON body, or throw an ApiError with the
// message sent by the API (or a readable one when the body is not JSON)
async function apiRequest(path, options = {}) {
  const { body, ...fetchOptions } = options;
  if (body !== undefined) {
    fetchOptions.headers = { "Content-Type": "application/json" };
    fetchOptions.body = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, fetchOptions);
  } catch (error) {
    throw new ApiError(
      "Cannot reach the server. Check that the API is running."
    );
  }

  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch (error) {
    data = null; // Flask HTML error page
  }

  if (!response.ok || (data && data.error)) {
    const message =
      (data && data.error) ||
      `Request failed (${response.status} ${response.statusText})`;
    throw new ApiError(message, response.status);
  }
  if (data === null) {
    throw new ApiError("The server sent an invalid response.", response.status);
  }
  return data;
}

// Tell the user that an action failed, with the cause given by the API
function reportError(action, error) {
  console.error(`${action}:`, error);
  alert(`${action}: ${error.message}`);
}

// Delete a board on the server, ignoring failures (the server also drops
// unused boards after a while)
function deleteBoardOnServer(boardId, keepalive = false) {
  fetch(`${API_BASE}/board/${boardId}`, { method: "DELETE", keepalive }).catch(
    () => {}
  );
}

// Use a new board returned by the API and forget the previous one
function replaceBoard(boardId, board) {
  const previousId = state.boardId;
  state.boardId = boardId;
  state.board = board;
  state.initialBoard = null;
  state.stepCount = 0;
  document.getElementById("log-container").innerHTML = "";
  if (previousId && previousId !== boardId) {
    deleteBoardOnServer(previousId);
  }

  renderGrid(state.mode === "solver" ? "sudoku-grid-solver" : "sudoku-grid");
  updateActiveConstraints();
  updateBoardStatus();
}

// Board in the JSON format of the API (size, cells, constraints)
function boardToExport(board) {
  const cells = {};
  board.cells.forEach((cell) => {
    cells[cell.pos] = cell.is_filled ? [cell.value] : [...cell.candidates];
  });
  return {
    size: board.size,
    cells,
    constraints: JSON.parse(JSON.stringify(board.constraints || [])),
  };
}

// Initialize application
document.addEventListener("DOMContentLoaded", async () => {
  await loadConstraints();
  setupEventListeners();
  createGrid("sudoku-grid");
  createGrid("sudoku-grid-solver");
  initializeBoard();
});

// Free the board on the server when the page is closed
window.addEventListener("pagehide", () => {
  if (state.boardId) {
    deleteBoardOnServer(state.boardId, true);
  }
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
}

// Switch between setup and solver modes
function switchMode(mode) {
  state.mode = mode;

  // Update mode buttons
  document
    .querySelectorAll(".mode-btn")
    .forEach((btn) => btn.classList.remove("active"));
  document.getElementById(`${mode}-mode-btn`).classList.add("active");

  // Update mode panels
  document
    .querySelectorAll(".mode-panel")
    .forEach((panel) => panel.classList.remove("active"));
  document.getElementById(`${mode}-mode`).classList.add("active");

  if (mode === "solver") {
    // Save initial board state when entering solver mode
    state.initialBoard = state.board ? boardToExport(state.board) : null;
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
    const data = await apiRequest("/constraints");
    state.constraints = data.constraints;
    renderConstraintList();
  } catch (error) {
    console.error("Failed to load constraints:", error);
    const list = document.getElementById("constraint-list");
    list.textContent = `Failed to load constraints: ${error.message}`;
  }
}

// Render constraint list in setup mode
function renderConstraintList() {
  const list = document.getElementById("constraint-list");
  list.innerHTML = "";

  state.constraints.forEach((constraint) => {
    const item = document.createElement("div");
    item.className = "constraint-item";
    item.textContent = constraint.name.replace("Constraint", "");
    item.addEventListener("click", () => selectConstraint(constraint));
    list.appendChild(item);
  });
}

// Select a constraint type
function selectConstraint(constraint) {
  state.selectedConstraint = constraint;

  // Update UI
  document
    .querySelectorAll(".constraint-item")
    .forEach((item) => item.classList.remove("selected"));
  event.target.classList.add("selected");

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
            <label>Select cells on the grid</label>
            <p style="font-size: 12px; color: #666;">Click cells to select them for this constraint</p>
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
    const data = await apiRequest("/board/new", {
      method: "POST",
      body: boardData,
    });
    replaceBoard(data.board_id, data.board);
  } catch (error) {
    reportError("Failed to create the board", error);
  }
}

// Create grid DOM elements
function createGrid(gridId) {
  const grid = document.getElementById(gridId);
  grid.innerHTML = "";

  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = row;
      cell.dataset.col = col;
      cell.dataset.pos = String.fromCharCode(97 + row) + (col + 1);

      if (gridId === "sudoku-grid") {
        cell.addEventListener("click", () => handleCellClick(cell));
      } else {
        cell.addEventListener("click", () => handleSolverCellClick(cell));
      }

      grid.appendChild(cell);
    }
  }
}

// Handle cell click in setup mode
function handleCellClick(cellElement) {
  const pos = cellElement.dataset.pos;

  // Toggle selection
  if (state.selectedCells.includes(pos)) {
    state.selectedCells = state.selectedCells.filter((p) => p !== pos);
    cellElement.classList.remove("selected");
  } else {
    state.selectedCells.push(pos);
    cellElement.classList.add("selected");
  }
}

// Handle cell click in solver mode
function handleSolverCellClick(cellElement) {
  const pos = cellElement.dataset.pos;
  const value = prompt(
    `Enter value for cell ${pos.toUpperCase()} (1-9) or leave empty to clear:`
  );

  if (value === null) return; // Cancelled

  if (value === "" || value === "0") {
    // Clear cell - reset to all candidates
    updateCell(pos, null, [1, 2, 3, 4, 5, 6, 7, 8, 9]);
  } else {
    const num = parseInt(value);
    if (num >= 1 && num <= 9) {
      updateCell(pos, num, [num]);
    } else {
      alert("Invalid value. Please enter a number between 1 and 9.");
    }
  }
}

// Update cell value
async function updateCell(pos, value, candidates) {
  try {
    const data = await apiRequest(`/board/${state.boardId}/cell`, {
      method: "PUT",
      body: { pos, value, candidates },
    });
    state.board = data.board;
    renderGrid("sudoku-grid-solver");
    updateBoardStatus();
  } catch (error) {
    reportError(`Failed to update cell ${pos.toUpperCase()}`, error);
  }
}

// Add constraint to board
async function addConstraint() {
  if (!state.selectedConstraint) {
    alert("Please select a constraint type.");
    return;
  }

  // Global constraints don't require cell selection
  const globalConstraints = ["knight", "king", "universal"];
  if (
    !globalConstraints.includes(state.selectedConstraint.id) &&
    state.selectedCells.length === 0
  ) {
    alert("Please select at least one cell.");
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
      alert("Kropki constraint requires exactly 2 adjacent cells.");
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
      alert("XV constraint requires exactly 2 adjacent cells.");
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
      alert("Parity constraint requires exactly 1 cell.");
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
      alert("GreaterThan constraint requires exactly 2 adjacent cells.");
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
    const data = await apiRequest(`/board/${state.boardId}/constraint`, {
      method: "POST",
      body: constraintData,
    });

    state.board = data.board;
    renderGrid("sudoku-grid");
    renderConstraints("sudoku-grid", state.board.constraints);
    updateActiveConstraints();

    // Clear selection
    state.selectedCells = [];
    document
      .querySelectorAll(".cell.selected")
      .forEach((cell) => cell.classList.remove("selected"));

    console.log(
      `Constraint "${state.selectedConstraint.name}" added successfully`
    );
  } catch (error) {
    reportError("Failed to add constraint", error);
  }
}

// Update active constraints display
function updateActiveConstraints() {
  const list = document.getElementById("constraint-list-display");
  list.innerHTML = "";

  if (!state.board || !state.board.constraints) return;

  state.board.constraints.forEach((constraint, index) => {
    const item = document.createElement("li");
    item.innerHTML = `
            <span>${constraint.type}</span>
            <span class="constraint-delete" data-index="${index}">✕</span>
        `;

    // Add click handler for delete button
    const deleteBtn = item.querySelector(".constraint-delete");
    deleteBtn.addEventListener("click", () => deleteConstraint(index));

    list.appendChild(item);
  });
}

// Delete constraint
async function deleteConstraint(index) {
  if (!confirm("Delete this constraint?")) return;

  try {
    const data = await apiRequest(
      `/board/${state.boardId}/constraint/${index}`,
      { method: "DELETE" }
    );
    state.board = data.board;
    renderGrid("sudoku-grid");
    updateActiveConstraints();
  } catch (error) {
    reportError("Failed to delete constraint", error);
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

  // Always redraw the constraint layer, so that an empty list clears it
  renderConstraints(gridId, state.board.constraints || []);
}

// Solve one step
async function solveStep() {
  const solverType = document.getElementById("solver-type").value;

  try {
    const data = await apiRequest(`/board/${state.boardId}/solve/step`, {
      method: "POST",
      body: { solver_type: solverType },
    });

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
      alert("🎉 Puzzle solved!");
    } else if (!data.changed) {
      alert("No progress made. Try a different solver or manual intervention.");
    }
  } catch (error) {
    reportError("Failed to execute solving step", error);
  }
}

// Auto solve
async function solveAuto() {
  if (state.autoSolving) return;
  const solverType = document.getElementById("solver-type").value;
  let maxSteps = 100;
  state.autoSolving = true;
  setSolverButtonsDisabled(true);

  try {
    while (maxSteps-- > 0) {
      const data = await apiRequest(`/board/${state.boardId}/solve/step`, {
        method: "POST",
        body: { solver_type: solverType },
      });

      state.board = data.board;
      state.stepCount++;

      addLogEntry(data.log, data.changed, data.solved);
      renderGrid("sudoku-grid-solver");
      updateBoardStatus();

      if (data.solved) {
        alert("🎉 Puzzle solved!");
        break;
      }

      if (!data.changed) {
        alert("Cannot make further progress automatically.");
        break;
      }

      // Small delay for visualization
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  } catch (error) {
    reportError("Auto solve stopped", error);
  } finally {
    state.autoSolving = false;
    setSolverButtonsDisabled(false);
  }
}

// Disable the solver buttons while auto solve is running
function setSolverButtonsDisabled(disabled) {
  ["solve-step-btn", "solve-auto-btn", "reset-board-btn"].forEach((id) => {
    document.getElementById(id).disabled = disabled;
  });
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

// Reset board to the state saved when entering solver mode, on the server too
async function resetBoard() {
  if (!state.initialBoard) return;

  try {
    const data = await apiRequest(`/board/${state.boardId}/reset`, {
      method: "POST",
      body: state.initialBoard,
    });
    state.board = data.board;
    state.stepCount = 0;
    renderGrid("sudoku-grid-solver");
    updateBoardStatus();
    document.getElementById("log-container").innerHTML = "";
  } catch (error) {
    reportError("Failed to reset the board", error);
  }
}

// Clear board
async function clearBoard() {
  if (confirm("Clear the entire board?")) {
    state.selectedCells = [];
    document
      .querySelectorAll(".cell.selected")
      .forEach((cell) => cell.classList.remove("selected"));
    await initializeBoard();
  }
}

// Export board
async function exportBoard() {
  if (!state.boardId) return;

  let data;
  try {
    data = await apiRequest(`/board/${state.boardId}/export`);
  } catch (error) {
    reportError("Failed to export the board", error);
    return;
  }

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

// Show modal for constraint parameters
function showConstraintParamModal(title, fields) {
  return new Promise((resolve) => {
    const modal = document.getElementById("constraint-param-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");
    const okBtn = document.getElementById("modal-ok");
    const cancelBtn = document.getElementById("modal-cancel");

    modalTitle.textContent = title;
    modalBody.innerHTML = "";

    // Create form fields
    fields.forEach((field) => {
      const label = document.createElement("label");
      label.textContent = field.label;
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

    const cleanup = () => {
      modal.classList.remove("active");
      okBtn.removeEventListener("click", handleOk);
      cancelBtn.removeEventListener("click", handleCancel);
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

    okBtn.addEventListener("click", handleOk);
    cancelBtn.addEventListener("click", handleCancel);
  });
}

// Import board
async function importBoard(event) {
  const input = event.target;
  const file = input.files[0];
  // Allow choosing the same file again after an error
  input.value = "";
  if (!file) return;

  let data;
  try {
    data = JSON.parse(await file.text());
  } catch (error) {
    reportError("Failed to import board", new Error("The file is not valid JSON."));
    return;
  }

  try {
    const result = await apiRequest("/board/new", {
      method: "POST",
      body: data,
    });
    replaceBoard(result.board_id, result.board);
    alert("Board imported successfully!");
  } catch (error) {
    // The previous board is kept and stays usable
    reportError("Failed to import board", error);
  }
}
