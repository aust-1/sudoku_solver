getLink = function () {
  return location.origin + location.pathname + importString + exportPuzzle();
};

exportPuzzle = function (includeCandidates) {
  const puzzle = { size };

  // Info

  if (customTitle.length) puzzle.title = customTitle;
  if (author.length) puzzle.author = author;
  if (customRuleset.length) puzzle.ruleset = customRuleset;
  if (disableHC) puzzle.highlightConflicts = false;

  // Grid

  puzzle.grid = [];
  for (var i = 0; i < size; i++) {
    puzzle.grid.push([]);
    for (var j = 0; j < size; j++) {
      puzzle.grid[i][j] = {};
      if (includeCandidates)
        puzzle.grid[i][j].candidates = grid[i][j].candidates;
      if (
        grid[i][j].region !==
        Math.floor(grid[i][j].i / regionH) * regionH +
          Math.floor(grid[i][j].j / regionW)
      )
        puzzle.grid[i][j].region = grid[i][j].region;

      if (grid[i][j].value) puzzle.grid[i][j].value = grid[i][j].value;
      if (grid[i][j].given) puzzle.grid[i][j].given = grid[i][j].given;
      if (grid[i][j].cornerPencilMarks.length)
        puzzle.grid[i][j].cornerPencilMarks = grid[i][j].cornerPencilMarks;
      if (grid[i][j].centerPencilMarks.length)
        puzzle.grid[i][j].centerPencilMarks = grid[i][j].centerPencilMarks;
      if (grid[i][j].c) puzzle.grid[i][j].c = highlightCs[grid[i][j].c];
      if (grid[i][j].highlight)
        puzzle.grid[i][j].highlight = highlightCs[grid[i][j].highlight];
    }
  }

  // Boolean Constraints

  for (var a = 0; a < boolConstraints.length; a++) {
    if (constraints[cID(boolConstraints[a])])
      puzzle[cID(boolConstraints[a])] = true;
  }

  // Tool Constraints

  for (var a = 0; a < toolConstraints.length; a++) {
    if (
      constraints[cID(toolConstraints[a])].length ||
      constraints[cID(toolConstraints[a])].negative
    ) {
      const constraint = constraints[cID(toolConstraints[a])];

      if (constraint.negative) {
        if (!puzzle.negative) puzzle.negative = [];
        puzzle.negative.push(cID(toolConstraints[a]));
      }

      puzzle[cID(toolConstraints[a])] = [];
      for (var b = 0; b < constraint.length; b++) {
        puzzle[cID(toolConstraints[a])].push({});

        if (constraint[b].lines)
          puzzle[cID(toolConstraints[a])][b].lines = constraint[b].lines.map(
            (c) => c.map((d) => formatCell(d))
          );
        if (constraint[b].cell)
          puzzle[cID(toolConstraints[a])][b].cell = formatCell(
            constraint[b].cell
          );
        if (constraint[b].cells)
          puzzle[cID(toolConstraints[a])][b].cells = constraint[b].cells.map(
            (c) => formatCell(c)
          );
        if (constraint[b].cloneCells)
          puzzle[cID(toolConstraints[a])][b].cloneCells = constraint[
            b
          ].cloneCells.map((c) => formatCell(c));
        if (constraint[b].direction)
          puzzle[cID(toolConstraints[a])][b].direction =
            constraint[b].direction;
        if (constraint[b].value)
          puzzle[cID(toolConstraints[a])][b].value = constraint[b].value;
        if (constraint[b].values)
          puzzle[cID(toolConstraints[a])][b].values = constraint[b].values;
      }
    }
  }

  // Cosmetics

  for (var a = 0; a < toolCosmetics.length; a++) {
    if (
      cosmetics[cID(toolCosmetics[a])].length ||
      cosmetics[cID(toolCosmetics[a])].negative
    ) {
      const cosmetic = cosmetics[cID(toolCosmetics[a])];

      puzzle[cID(toolCosmetics[a])] = [];
      for (var b = 0; b < cosmetic.length; b++) {
        puzzle[cID(toolCosmetics[a])].push({});

        if (cosmetic[b].lines)
          puzzle[cID(toolCosmetics[a])][b].lines = cosmetic[b].lines.map((c) =>
            c.map((d) => formatCell(d))
          );
        if (cosmetic[b].cell)
          puzzle[cID(toolCosmetics[a])][b].cell = formatCell(cosmetic[b].cell);
        if (cosmetic[b].cells)
          puzzle[cID(toolCosmetics[a])][b].cells = cosmetic[b].cells.map((c) =>
            formatCell(c)
          );
        if (cosmetic[b].direction)
          puzzle[cID(toolCosmetics[a])][b].direction = cosmetic[b].direction;
        if (cosmetic[b].value)
          puzzle[cID(toolCosmetics[a])][b].value = cosmetic[b].value;
        if (cosmetic[b].baseC)
          puzzle[cID(toolCosmetics[a])][b].baseC = cosmetic[b].baseC;
        if (cosmetic[b].outlineC)
          puzzle[cID(toolCosmetics[a])][b].outlineC = cosmetic[b].outlineC;
        if (cosmetic[b].fontC)
          puzzle[cID(toolCosmetics[a])][b].fontC = cosmetic[b].fontC;
        if (cosmetic[b].size)
          puzzle[cID(toolCosmetics[a])][b].size = cosmetic[b].size;
        if (cosmetic[b].width)
          puzzle[cID(toolCosmetics[a])][b].width = cosmetic[b].width;
        if (cosmetic[b].height)
          puzzle[cID(toolCosmetics[a])][b].height = cosmetic[b].height;
        if (cosmetic[b].angle)
          puzzle[cID(toolCosmetics[a])][b].angle = cosmetic[b].angle;
      }
    }
  }

  return compressor.compressToBase64(JSON.stringify(puzzle));
};

importPuzzle = function (string, clearHistory) {
  const oldSize = size;
  const oldSelection = selection.map((a) => formatCell(a));

  const puzzle = JSON.parse(compressor.decompressFromBase64(string));

  // Info

  customTitle = "";
  author = "";
  customRuleset = "";
  if (puzzle.title) customTitle = puzzle.title;
  if (puzzle.author) author = puzzle.author;
  if (puzzle.ruleset) customRuleset = puzzle.ruleset;
  if (puzzle.highlightConflicts !== undefined)
    boolSettings["Highlight Conflicts"] = false;

  // Grid

  createGrid(puzzle.size, clearHistory, clearHistory);

  for (var i = 0; i < size; i++) {
    for (var j = 0; j < size; j++) {
      if (puzzle.grid[i][j].region !== undefined)
        grid[i][j].region = puzzle.grid[i][j].region;
      if (puzzle.grid[i][j].candidates)
        grid[i][j].candidates = puzzle.grid[i][j].candidates;
      else addAllCandidates(grid[i][j]);

      if (puzzle.grid[i][j].value) grid[i][j].value = puzzle.grid[i][j].value;
      if (puzzle.grid[i][j].given) grid[i][j].given = puzzle.grid[i][j].given;
      if (puzzle.grid[i][j].cornerPencilMarks)
        grid[i][j].cornerPencilMarks = puzzle.grid[i][j].cornerPencilMarks;
      if (puzzle.grid[i][j].centerPencilMarks)
        grid[i][j].centerPencilMarks = puzzle.grid[i][j].centerPencilMarks;
      if (puzzle.grid[i][j].c)
        grid[i][j].c = highlightCs.indexOf(puzzle.grid[i][j].c);
      if (puzzle.grid[i][j].highlight)
        grid[i][j].highlight = highlightCs.indexOf(puzzle.grid[i][j].highlight);
    }
  }

  // Boolean Constraints

  for (var a = 0; a < boolConstraints.length; a++) {
    if (puzzle[cID(boolConstraints[a])])
      constraints[cID(boolConstraints[a])] = true;
  }

  // Tool Constraints

  for (var a = 0; a < toolConstraints.length; a++) {
    if (puzzle[cID(toolConstraints[a])]) {
      const constraint = puzzle[cID(toolConstraints[a])];

      for (var b = 0; b < constraint.length; b++) {
        constraints[cID(toolConstraints[a])].push(
          new window[cID(toolConstraints[a])]()
        );

        if (constraint[b].lines)
          constraints[cID(toolConstraints[a])][b].lines = constraint[
            b
          ].lines.map((c) => c.map((d) => unformatCell(d)));
        if (constraint[b].cell)
          constraints[cID(toolConstraints[a])][b].cell = unformatCell(
            constraint[b].cell
          );
        if (constraint[b].cells)
          constraints[cID(toolConstraints[a])][b].cells = constraint[
            b
          ].cells.map((c) => unformatCell(c));
        if (constraint[b].cloneCells)
          constraints[cID(toolConstraints[a])][b].cloneCells = constraint[
            b
          ].cloneCells.map((c) => unformatCell(c));
        if (constraint[b].direction)
          constraints[cID(toolConstraints[a])][b].direction =
            constraint[b].direction;
        if (constraint[b].value)
          constraints[cID(toolConstraints[a])][b].value = constraint[b].value;
        if (constraint[b].values)
          constraints[cID(toolConstraints[a])][b].values = constraint[b].values;

        if (constraints[cID(toolConstraints[a])][b].updateSet)
          constraints[cID(toolConstraints[a])][b].updateSet();
      }
    }
  }

  // Negative Constraints

  if (puzzle.negative) {
    for (var a = 0; a < puzzle.negative.length; a++) {
      const cid = cID(puzzle.negative[a]);
      constraints[cid] ||= {};
      constraints[cid].negative = true;
    }
  }

  // Cosmetics

  for (var a = 0; a < toolCosmetics.length; a++) {
    if (puzzle[cID(toolCosmetics[a])]) {
      const cosmetic = puzzle[cID(toolCosmetics[a])];

      for (var b = 0; b < cosmetic.length; b++) {
        cosmetics[cID(toolCosmetics[a])].push(
          new window[cID(toolCosmetics[a])]()
        );

        if (cosmetic[b].lines)
          cosmetics[cID(toolCosmetics[a])][b].lines = cosmetic[b].lines.map(
            (c) => c.map((d) => unformatCell(d))
          );
        if (cosmetic[b].cell)
          cosmetics[cID(toolCosmetics[a])][b].cell = unformatCell(
            cosmetic[b].cell
          );
        if (cosmetic[b].cells)
          cosmetics[cID(toolCosmetics[a])][b].cells = cosmetic[b].cells.map(
            (c) => unformatCell(c)
          );
        if (cosmetic[b].direction)
          cosmetics[cID(toolCosmetics[a])][b].direction = cosmetic[b].direction;
        if (cosmetic[b].value)
          cosmetics[cID(toolCosmetics[a])][b].value = cosmetic[b].value;
        if (cosmetic[b].baseC)
          cosmetics[cID(toolCosmetics[a])][b].baseC = cosmetic[b].baseC;
        if (cosmetic[b].outlineC)
          cosmetics[cID(toolCosmetics[a])][b].outlineC = cosmetic[b].outlineC;
        if (cosmetic[b].fontC)
          cosmetics[cID(toolCosmetics[a])][b].fontC = cosmetic[b].fontC;
        if (cosmetic[b].size)
          cosmetics[cID(toolCosmetics[a])][b].size = cosmetic[b].size;
        if (cosmetic[b].width)
          cosmetics[cID(toolCosmetics[a])][b].width = cosmetic[b].width;
        if (cosmetic[b].height)
          cosmetics[cID(toolCosmetics[a])][b].height = cosmetic[b].height;
        if (cosmetic[b].angle)
          cosmetics[cID(toolCosmetics[a])][b].angle = cosmetic[b].angle;
      }
    }
  }

  // Convert Outdated Versions

  const oldHighlightCs = [
    "#FFFFFF",
    "#A8A8A8",
    "#000000",
    "#FFA0A0",
    "#FFE060",
    "#FFFFB0",
    "#B0FFB0",
    "#D0D0FF",
    "#FF80FF",
  ];
  for (var i = 0; i < size; i++) {
    for (var j = 0; j < size; j++) {
      if (puzzle.grid[i][j].c === parseInt(puzzle.grid[i][j].c))
        grid[i][j].c = highlightCs.indexOf(oldHighlightCs[puzzle.grid[i][j].c]);
      if (puzzle.grid[i][j].highlight === parseInt(puzzle.grid[i][j].highlight))
        grid[i][j].highlight = highlightCs.indexOf(
          oldHighlightCs[puzzle.grid[i][j].highlight]
        );

      if (puzzle.grid[i][j].parity)
        constraints[cID(puzzle.grid[i][j].parity)].push(
          new window[cID(puzzle.grid[i][j].parity)]([grid[i][j]])
        );
      if (puzzle.grid[i][j].extreme)
        constraints[cID(puzzle.grid[i][j].extreme)].push(
          new window[cID(puzzle.grid[i][j].extreme)]([grid[i][j]])
        );
    }
  }

  if (clearHistory) {
    generateCandidates();
    resetKnownPuzzleInformation();
    clearChangeHistory();
  }

  if (oldSize === size) selection = oldSelection.map((a) => unformatCell(a));
};
