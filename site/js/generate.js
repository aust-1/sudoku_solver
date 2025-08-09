generateSolution = function () {
  solve({ bruteForce: true, random: true });
};

generateGivens = function (options) {
  time = 0;
  if (!options) options = {};
  if (options.difficulty) options.logicOnly = true;
  if (parseInt(options.difficulty) === options.difficulty)
    options.difficulty = [options.difficulty, options.difficulty];
  else options.difficulty = [1, 3];
  if (!options.symmetry) options.symmetry = [];

  var cells = getCells();

  highlighted = cells.some((a) => a.c);

  difficultyReached = false;
  var attempts = 0;
  var impossible = false;
  do {
    impossible = false;

    if (attempts >= generationAttempts) {
      clearConsole();
      cells.forEach((a) => (a.given = false));
      clearGrid();
      log(generationAttempts + " attempts reached; Generation cancelled");
      onInputEnd(); // Remove if a button is added
      return;
    }

    cells.forEach((a) => (a.given = false));
    clearGrid();
    generateSolution();

    difficulty = 1;

    if (solveOutput === "Solved") {
      cells.forEach((a) => {
        if (
          (highlighted && !a.c) ||
          (constraints[cID("Diagonal +")] && a.i === size - a.j - 1) ||
          (constraints[cID("Diagonal -")] && a.i === a.j) ||
          a.parity ||
          a.extreme ||
          multicellConstraints.some(
            (b) =>
              constraints[cID(b)].some(
                (c) => c.lines && c.lines.some((d) => d.includes(a))
              ) ||
              constraints[cID(b)].some((c) => c.cells && c.cells.includes(a)) ||
              constraints[cID(b)].some(
                (c) => c.cloneCells && c.cloneCells.includes(a)
              )
          )
        ) {
          a.value = 0;
          a.given = false;
        } else a.given = true;
      });
      cells.forEach((a) => {
        if (
          getSymmetricalCoords([a], options.symmetry)
            .map((b) => grid[b.i][b.j])
            .some((b) => !b.given)
        )
          a.given = false;
      });

      removableCells = cells.filter((a) => a.value);
      var i = null;
      var j = null;

      var iterations = 0;
      do {
        do {
          i = Math.floor(Math.random() * size);
          j = Math.floor(Math.random() * size);
        } while (!removableCells.includes(grid[i][j]));
        const coords = generateCoords(i, j, options.symmetry);

        coords.forEach((a) => {
          grid[a.i][a.j].backupValue = grid[a.i][a.j].value;
          if (iterations >= 1) {
            grid[a.i][a.j].value = 0;
            grid[a.i][a.j].given = false;

            if (removableCells.includes(grid[a.i][a.j]))
              removableCells.splice(removableCells.indexOf(grid[a.i][a.j]), 1);
          }
        });

        clearGrid();

        var difficultyBackup = difficulty;
        if (options.logicOnly)
          solve({
            logicOnly: true,
            logProgress: false,
            difficultyLimit: options.difficulty[1],
          });
        if (
          options.logicOnly
            ? solveOutput !== "Solved"
            : countSolutions(
                { difficultyLimit: options.difficulty[1] },
                true
              ) !== 1
        ) {
          if (iterations >= 1) {
            coords.forEach((a) => {
              grid[a.i][a.j].value = grid[a.i][a.j].backupValue;
              grid[a.i][a.j].given = true;
            });
          }

          difficulty = difficultyBackup;
          if (!iterations) {
            impossible = true;
            break;
          }
        } else {
          if (!iterations) difficulty = 1;
          if (difficulty >= options.difficulty[0]) difficultyReached = true;
        }

        changeUndo = false;
        iterations++;
      } while (!highlighted && removableCells.length);
    } else {
      clearConsole();
      log(formatSolveOutcome(solveOutput));
      onInputEnd(); // Remove if a button is added
      return;
    }

    clearGrid();
    if (impossible) console.log("Rejected a puzzle that was impossible");
    else if (options.difficulty && difficulty < options.difficulty[0])
      console.log("Rejected a puzzle that was too easy");
    else if (
      options.maxGivens &&
      getCells().filter((a) => a.given).length > options.maxGivens
    )
      console.log("Rejected a puzzle that had too many givens");

    attempts++;
  } while (
    (options.difficulty && !difficultyReached) ||
    (options.maxGivens &&
      getCells().filter((a) => a.given).length > options.maxGivens) ||
    impossible
  );

  clearConsole();
  log(
    "Successfully generated given digits" +
      (options.difficulty ? " with difficulty " + difficulty + "/4" : "")
  );
  onInputEnd(); // Remove if a button is added
};

generateCoords = function (i, j, symmetry) {
  const coords = [{ i, j }];

  var changed = false;
  do {
    changed = false;

    const newCoords = getSymmetricalCoords(coords, symmetry);

    for (var a = 0; a < newCoords.length; a++) {
      if (
        coords.findIndex(
          (b) => b.i === newCoords[a].i && b.j === newCoords[a].j
        ) === -1
      ) {
        coords.push(newCoords[a]);
        changed = true;
      }
    }
  } while (changed);

  return coords;
};

getSymmetricalCoords = function (coords, symmetry) {
  time -= new Date().getTime();
  const newCoords = [];
  for (var a = 0; a < coords.length; a++) {
    if (symmetry.includes("90")) {
      newCoords.push({ i: coords[a].j, j: size - coords[a].i - 1 });
      newCoords.push({ i: size - coords[a].i - 1, j: size - coords[a].j - 1 });
      newCoords.push({ i: size - coords[a].j - 1, j: coords[a].i });
    }
    if (symmetry.includes("180"))
      newCoords.push({ i: size - coords[a].i - 1, j: size - coords[a].j - 1 });
    if (symmetry.includes("H"))
      newCoords.push({ i: size - coords[a].i - 1, j: coords[a].j });
    if (symmetry.includes("V"))
      newCoords.push({ i: coords[a].i, j: size - coords[a].j - 1 });
    if (symmetry.includes("+"))
      newCoords.push({ i: size - coords[a].j - 1, j: size - coords[a].i - 1 });
    if (symmetry.includes("-"))
      newCoords.push({ i: coords[a].j, j: coords[a].i });
  }
  time += new Date().getTime();
  return newCoords;
};

generatePuzzleSet = function (amount, options) {
  if (!options) options = {};

  for (var a = 0; a < amount; a++) {
    var usedOptions = JSON.parse(JSON.stringify(options));
    if (!usedOptions.difficulty)
      usedOptions.difficulty = 1 + Math.floor((5 * a) / amount);
    if (!usedOptions.symmetry)
      usedOptions.symmetry =
        symmetries[Math.floor(Math.random() * symmetries.length)];

    console.log(
      "Beginning the generation of puzzle #" +
        (a + 1) +
        ";  Difficulty: " +
        usedOptions.difficulty +
        ";  Symmetry: " +
        usedOptions.symmetry
    );
    generateGivens(usedOptions);
    console.log("Successfully generated puzzle #" + (a + 1));
    download(false, getPuzzleTitle() + " #" + (a + 1));
  }
};
