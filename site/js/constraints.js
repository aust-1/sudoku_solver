getCellsSeenByCell = function (cell, nested) {
  const seen = new Set();

  if (!nested) {
    constraints[cID("Palindrome")].forEach((a) => (a.considered = false));
    constraints[cID("Clone")].forEach((a) => (a.considered = false));
  }

  getCellsSeenByRow(cell).forEach((a) => seen.add(a));
  getCellsSeenByColumn(cell).forEach((a) => seen.add(a));
  getCellsSeenByRegion(cell).forEach((a) => seen.add(a));
  getCellsSeenByDiagonal(cell).forEach((a) => seen.add(a));
  getCellsSeenByKnightsMove(cell).forEach((a) => seen.add(a));
  getCellsSeenByKingsMove(cell).forEach((a) => seen.add(a));
  getCellsSeenByDisjointGroup(cell).forEach((a) => seen.add(a));
  getCellsSeenByExtraRegion(cell).forEach((a) => seen.add(a));
  getCellsSeenByKillerCage(cell).forEach((a) => seen.add(a));

  var added = false;
  do {
    added = false;

    seen.forEach((a) => {
      for (var b = 0; b < constraints[cID("Palindrome")].length; b++) {
        currentPalindrome = constraints[cID("Palindrome")][b].lines[0];
        if (
          currentPalindrome.includes(a) &&
          !seen.has(
            currentPalindrome[
              currentPalindrome.length - currentPalindrome.indexOf(a) - 1
            ]
          )
        ) {
          seen.add(
            currentPalindrome[
              currentPalindrome.length - currentPalindrome.indexOf(a) - 1
            ]
          );
          added = true;
        }
      }
    });

    seen.forEach((a) => {
      for (var b = 0; b < constraints[cID("Clone")].length; b++) {
        currentClone = constraints[cID("Clone")][b];
        if (
          currentClone.cells.includes(a) &&
          !seen.has(currentClone.cloneCells[currentClone.cells.indexOf(a)])
        ) {
          seen.add(currentClone.cloneCells[currentClone.cells.indexOf(a)]);
          added = true;
        }
        if (
          currentClone.cloneCells.includes(a) &&
          !seen.has(currentClone.cells[currentClone.cloneCells.indexOf(a)])
        ) {
          seen.add(currentClone.cells[currentClone.cloneCells.indexOf(a)]);
          added = true;
        }
      }
    });
  } while (added);

  for (var a = 0; a < constraints[cID("Palindrome")].length; a++) {
    currentPalindrome = constraints[cID("Palindrome")][a].lines[0];
    if (
      currentPalindrome.includes(cell) &&
      !constraints[cID("Palindrome")][a].considered
    ) {
      constraints[cID("Palindrome")][a].considered = true;
      getCellsSeenByCell(
        currentPalindrome[
          currentPalindrome.length - currentPalindrome.indexOf(cell) - 1
        ],
        true
      ).forEach((b) => seen.add(b));
    }
  }

  for (var a = 0; a < constraints[cID("Clone")].length; a++) {
    currentClone = constraints[cID("Clone")][a];
    if (!constraints[cID("Clone")][a].considered) {
      if (currentClone.cells.includes(cell)) {
        constraints[cID("Clone")][a].considered = true;
        getCellsSeenByCell(
          currentClone.cloneCells[currentClone.cells.indexOf(cell)],
          true
        ).forEach((b) => seen.add(b));
      }
      if (currentClone.cloneCells.includes(cell)) {
        constraints[cID("Clone")][a].considered = true;
        getCellsSeenByCell(
          currentClone.cells[currentClone.cloneCells.indexOf(cell)],
          true
        ).forEach((b) => seen.add(b));
      }
    }
  }

  return Array.from(seen);
};

getCellsSeenByCells = function (cells) {
  if (!cells.length) return [];

  var cells = cells.map((a) => getCellsSeenByCell(a));

  const seen = cells.shift();
  return seen.filter((a) => cells.every((b) => b.includes(a)));
};

getEmptyCellsSeenByCell = function (cell) {
  return getCellsSeenByCell(cell).filter((a) => !a.value);
};

getEmptyCellsSeenByCells = function (cells) {
  return getCellsSeenByCells(cells).filter((a) => !a.value);
};

getCellsOrthogonalToAndIncludingCell = function (cell) {
  const seen = [];

  seen.push(cell);
  if (grid[cell.i - 1]) seen.push(grid[cell.i - 1][cell.j]);
  if (grid[cell.i][cell.j + 1]) seen.push(grid[cell.i][cell.j + 1]);
  if (grid[cell.i + 1]) seen.push(grid[cell.i + 1][cell.j]);
  if (grid[cell.i][cell.j - 1]) seen.push(grid[cell.i][cell.j - 1]);

  return seen;
};

getEmptyCellsOrthogonalToAndIncludingCell = function (cell) {
  return getCellsOrthogonalToAndIncludingCell(cell).filter((a) => !a.value);
};

getEmptyCellsOrthogonalToAndIncludingCells = function (cells) {
  if (!cells.length) return [];

  var cells = cells.map((a) => getEmptyCellsOrthogonalToAndIncludingCell(a));

  const seen = cells.shift();
  return seen.filter((a) => cells.every((b) => b.includes(a)));
};

getCellsSeenByRow = function (cell, returnIfFound) {
  const cells = [];
  for (var j = 0; j < size; j++) {
    if (j !== cell.j) {
      if (grid[cell.i][j].value === returnIfFound) return grid[cell.i][j];
      cells.push(grid[cell.i][j]);
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByColumn = function (cell, returnIfFound) {
  const cells = [];
  for (var i = 0; i < size; i++) {
    if (i !== cell.i) {
      if (grid[i][cell.j].value === returnIfFound) return grid[i][cell.j];
      cells.push(grid[i][cell.j]);
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByRegion = function (cell, returnIfFound) {
  const cells = [];
  if (cell.region !== null) {
    for (var i = 0; i < size; i++) {
      for (var j = 0; j < size; j++) {
        if (grid[i][j] !== cell && grid[i][j].region === cell.region) {
          if (grid[i][j].value === returnIfFound) return grid[i][j];
          cells.push(grid[i][j]);
        }
      }
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByDiagonal = function (cell, returnIfFound) {
  const cells = [];
  if (constraints[cID("Diagonal +")] && cell.i === size - cell.j - 1) {
    for (var i = 0; i < size; i++) {
      if (i !== cell.i) {
        if (grid[i][size - i - 1].value === returnIfFound)
          return grid[i][size - i - 1];
        cells.push(grid[i][size - i - 1]);
      }
    }
  }
  if (constraints[cID("Diagonal -")] && cell.i === cell.j) {
    for (var i = 0; i < size; i++) {
      if (i !== cell.i) {
        if (grid[i][i].value === returnIfFound) return grid[i][i];
        cells.push(grid[i][i]);
      }
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByKnightsMove = function (cell, returnIfFound) {
  const cells = [];
  if (constraints[cID("Antiknight")]) {
    const moves = [
      [-2, 1],
      [-1, 2],
      [1, 2],
      [2, 1],
      [2, -1],
      [1, -2],
      [-1, -2],
      [-2, -1],
    ];
    for (var a = 0; a < moves.length; a++) {
      if (
        grid[cell.i + moves[a][0]] &&
        grid[cell.i + moves[a][0]][cell.j + moves[a][1]]
      ) {
        if (
          grid[cell.i + moves[a][0]][cell.j + moves[a][1]].value ===
          returnIfFound
        )
          return grid[cell.i + moves[a][0]][cell.j + moves[a][1]];
        cells.push(grid[cell.i + moves[a][0]][cell.j + moves[a][1]]);
      }
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByKingsMove = function (cell, returnIfFound) {
  const cells = [];
  if (constraints[cID("Antiking")]) {
    const moves = [
      [-1, 1],
      [1, 1],
      [1, -1],
      [-1, -1],
    ];
    for (var a = 0; a < moves.length; a++) {
      if (
        grid[cell.i + moves[a][0]] &&
        grid[cell.i + moves[a][0]][cell.j + moves[a][1]]
      ) {
        if (
          grid[cell.i + moves[a][0]][cell.j + moves[a][1]].value ===
          returnIfFound
        )
          return grid[cell.i + moves[a][0]][cell.j + moves[a][1]];
        cells.push(grid[cell.i + moves[a][0]][cell.j + moves[a][1]]);
      }
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByDisjointGroup = function (cell, returnIfFound) {
  const cells = [];
  if (constraints[cID("Disjoint Groups")]) {
    const iOffset = cell.i % regionH;
    const jOffset = cell.j % regionW;
    for (var i = 0; i < size; i += regionH) {
      for (var j = 0; j < size; j += regionW) {
        if (i + iOffset !== cell.i || j + jOffset !== cell.j) {
          if (grid[i + iOffset][j + jOffset].value === returnIfFound)
            return grid[i + iOffset][j + jOffset];
          cells.push(grid[i + iOffset][j + jOffset]);
        }
      }
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByExtraRegion = function (cell, returnIfFound) {
  const cells = [];
  index = constraints[cID("Extra Region")].findIndex((a) =>
    a.cells.includes(cell)
  );
  if (index > -1) {
    for (
      var a = 0;
      a < constraints[cID("Extra Region")][index].cells.length;
      a++
    ) {
      if (cell !== constraints[cID("Extra Region")][index].cells[a]) {
        if (
          constraints[cID("Extra Region")][index].cells[a].value ===
          returnIfFound
        )
          return constraints[cID("Extra Region")][index].cells[a];
        cells.push(constraints[cID("Extra Region")][index].cells[a]);
      }
    }
  }

  return returnIfFound ? null : cells;
};

getCellsSeenByKillerCage = function (cell, returnIfFound) {
  const cells = [];
  index = constraints[cID("Killer Cage")].findIndex((a) =>
    a.cells.includes(cell)
  );
  if (index > -1) {
    for (
      var a = 0;
      a < constraints[cID("Killer Cage")][index].cells.length;
      a++
    ) {
      if (cell !== constraints[cID("Killer Cage")][index].cells[a]) {
        if (
          constraints[cID("Killer Cage")][index].cells[a].value ===
          returnIfFound
        )
          return constraints[cID("Killer Cage")][index].cells[a];
        cells.push(constraints[cID("Killer Cage")][index].cells[a]);
      }
    }
  }

  return returnIfFound ? null : cells;
};
