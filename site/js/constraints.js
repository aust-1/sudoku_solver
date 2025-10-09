// Constraint visualization for Sudoku CTC Solver Assistant

// SVG overlay for drawing constraints
let constraintSvg = null;

// Get actual cell size from the DOM
function getCellSize(gridId) {
  const grid = document.getElementById(gridId);
  const firstCell = grid.querySelector(".cell");
  if (firstCell) {
    return firstCell.getBoundingClientRect().width;
  }
  return 60; // fallback
}

// Initialize constraint visualization layer
function initConstraintLayer(gridId) {
  const grid = document.getElementById(gridId);

  // Remove existing SVG if present
  const existingSvg = grid.querySelector("svg.constraint-overlay");
  if (existingSvg) {
    existingSvg.remove();
  }

  // Get actual cell size from DOM
  const cellSize = getCellSize(gridId);

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.classList.add("constraint-overlay");
  svg.setAttribute("width", 9 * cellSize);
  svg.setAttribute("height", 9 * cellSize);
  svg.setAttribute("viewBox", `0 0 ${9 * cellSize} ${9 * cellSize}`);
  svg.style.position = "absolute";
  svg.style.top = "0";
  svg.style.left = "0";
  svg.style.pointerEvents = "none";
  svg.style.zIndex = "10";

  // Store cell size as data attribute for later use
  svg.dataset.cellSize = cellSize;

  grid.style.position = "relative";
  grid.appendChild(svg);

  return svg;
}

// Get cell center coordinates (cellSize from current SVG context)
function getCellCenter(row, col, cellSize = 60) {
  return {
    x: col * cellSize + cellSize / 2,
    y: row * cellSize + cellSize / 2,
  };
}

// Get position between two cells
function getPositionBetweenCells(cell1, cell2, cellSize = 60) {
  const pos1 = getCellCenter(cell1.row, cell1.col, cellSize);
  const pos2 = getCellCenter(cell2.row, cell2.col, cellSize);
  return {
    x: (pos1.x + pos2.x) / 2,
    y: (pos1.y + pos2.y) / 2,
  };
}

// Convert position string (e.g., "a1") to row/col
function posToRowCol(pos) {
  const row = pos.charCodeAt(0) - 97; // 'a' = 0
  const col = parseInt(pos.substring(1)) - 1;
  return { row, col };
}

// Draw a line through cells
function drawLine(svg, cells, color, width) {
  if (cells.length < 2) return;

  const cellSize = parseFloat(svg.dataset.cellSize) || 60;

  const points = cells
    .map((pos) => {
      const { row, col } = posToRowCol(pos);
      const center = getCellCenter(row, col, cellSize);
      return `${center.x},${center.y}`;
    })
    .join(" ");

  const polyline = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "polyline"
  );
  polyline.setAttribute("points", points);
  polyline.setAttribute(
    "stroke",
    `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${color[3] / 255})`
  );
  polyline.setAttribute("stroke-width", width);
  polyline.setAttribute("fill", "none");
  polyline.setAttribute("stroke-linecap", "round");
  polyline.setAttribute("stroke-linejoin", "round");

  svg.appendChild(polyline);
}

// Draw a killer cage
function drawKillerCage(svg, cells, sum, color) {
  if (cells.length === 0) return;

  const cellSize = parseFloat(svg.dataset.cellSize) || 60;

  // Convert cells to row/col coordinates
  const cellCoords = cells.map((pos) => posToRowCol(pos));

  // Draw cage outline (simplified - draws individual cell borders)
  cellCoords.forEach(({ row, col }) => {
    const x = col * cellSize;
    const y = row * cellSize;

    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", x);
    rect.setAttribute("y", y);
    rect.setAttribute("width", cellSize);
    rect.setAttribute("height", cellSize);
    rect.setAttribute(
      "fill",
      `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.1)`
    );
    rect.setAttribute(
      "stroke",
      `rgba(${color[0]}, ${color[1]}, ${color[2]}, 0.8)`
    );
    rect.setAttribute("stroke-width", "2");
    rect.setAttribute("stroke-dasharray", "5,5");

    svg.appendChild(rect);
  });

  // Draw sum label in top-left cell
  const firstCell = cellCoords[0];
  const x = firstCell.col * cellSize + 5;
  const y = firstCell.row * cellSize + 15;

  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", x);
  text.setAttribute("y", y);
  text.setAttribute("font-size", "12");
  text.setAttribute("font-weight", "bold");
  text.setAttribute("fill", `rgba(${color[0]}, ${color[1]}, ${color[2]}, 1)`);
  text.textContent = sum;

  svg.appendChild(text);
}

// Draw a circle between two cells
function drawCircleBetweenCells(svg, cell1Pos, cell2Pos, color) {
  const cellSize = parseFloat(svg.dataset.cellSize) || 60;
  const cell1 = posToRowCol(cell1Pos);
  const cell2 = posToRowCol(cell2Pos);
  const center = getPositionBetweenCells(cell1, cell2, cellSize);

  const circle = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "circle"
  );
  circle.setAttribute("cx", center.x);
  circle.setAttribute("cy", center.y);
  circle.setAttribute("r", "6"); // Smaller radius
  circle.setAttribute(
    "fill",
    `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${color[3] / 255})`
  );
  circle.setAttribute("stroke", color[0] === 255 ? "#333" : "none"); // White circles get dark border
  circle.setAttribute("stroke-width", color[0] === 255 ? "2" : "0");

  svg.appendChild(circle);
}

// Draw a circle in a cell
function drawCircleInCell(svg, cellPos, color) {
  const cellSize = parseFloat(svg.dataset.cellSize) || 60;
  const { row, col } = posToRowCol(cellPos);
  const center = getCellCenter(row, col, cellSize);

  const circle = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "circle"
  );
  circle.setAttribute("cx", center.x);
  circle.setAttribute("cy", center.y);
  circle.setAttribute("r", cellSize * 0.3); // Slightly smaller, better centered
  circle.setAttribute(
    "fill",
    `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${color[3] / 255})`
  );

  svg.appendChild(circle);
}

// Draw a square in a cell
function drawSquare(svg, cellPos, color) {
  const cellSize = parseFloat(svg.dataset.cellSize) || 60;
  const { row, col } = posToRowCol(cellPos);
  const center = getCellCenter(row, col, cellSize);
  const size = cellSize * 0.5; // Smaller, better proportioned

  const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  rect.setAttribute("x", center.x - size / 2);
  rect.setAttribute("y", center.y - size / 2);
  rect.setAttribute("width", size);
  rect.setAttribute("height", size);
  rect.setAttribute(
    "fill",
    `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${color[3] / 255})`
  );

  svg.appendChild(rect);
}

// Write text between two cells
function writeTextBetweenCells(svg, cell1Pos, cell2Pos, text) {
  const cellSize = parseFloat(svg.dataset.cellSize) || 60;
  const cell1 = posToRowCol(cell1Pos);
  const cell2 = posToRowCol(cell2Pos);
  const center = getPositionBetweenCells(cell1, cell2, cellSize);

  const textElement = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "text"
  );
  textElement.setAttribute("x", center.x);
  textElement.setAttribute("y", center.y);
  textElement.setAttribute("text-anchor", "middle");
  textElement.setAttribute("dominant-baseline", "middle");
  textElement.setAttribute("font-size", "16");
  textElement.setAttribute("font-weight", "bold");
  textElement.setAttribute("fill", "black");
  textElement.textContent = text;

  svg.appendChild(textElement);
}

// Render all constraints on a grid
function renderConstraints(gridId, constraints) {
  const svg = initConstraintLayer(gridId);

  if (!constraints || constraints.length === 0) return;

  constraints.forEach((constraint) => {
    renderConstraint(svg, constraint);
  });
}

// Render a single constraint
function renderConstraint(svg, constraint) {
  const type = constraint.type;

  switch (type) {
    case "killer":
      drawKillerCage(svg, constraint.cells, constraint.sum, constraint.color);
      break;

    case "palindrome":
      drawLine(svg, constraint.cells, [0, 140, 255, 120], 5);
      break;

    case "kropki":
      const color =
        constraint.color === "black" ? [0, 0, 0, 255] : [255, 255, 255, 255];
      drawCircleBetweenCells(svg, constraint.cell1, constraint.cell2, color);
      break;

    case "xv":
      const text = constraint.sum === 10 ? "X" : "V";
      writeTextBetweenCells(svg, constraint.cell1, constraint.cell2, text);
      break;

    case "bishop":
      // Bishop uses cells in the order they were selected (no diagonal ordering)
      if (constraint.cells && constraint.cells.length > 1) {
        drawLine(svg, constraint.cells, [0, 130, 255, 255], 2);
      }
      break;

    case "german":
      drawLine(svg, constraint.cells, [0, 255, 0, 120], 5);
      break;

    case "dutch":
      drawLine(svg, constraint.cells, [255, 154, 0, 120], 4);
      break;

    case "parity":
      const parityColor = [200, 200, 200, 156];
      if (constraint.rest === 1) {
        // Odd - draw circle
        drawCircleInCell(svg, constraint.cell, parityColor);
      } else {
        // Even - draw square
        drawSquare(svg, constraint.cell, parityColor);
      }
      break;

    // Knight, King, Universal, Clone, CloneZone, GreaterThan have no visual representation
    default:
      console.log(`No visualization for constraint type: ${type}`);
  }
}
