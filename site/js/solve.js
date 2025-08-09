var changed = false;
var possible = true;
var stop = false;
var solveOutput = null;

solve = function (options) {
  if (!options) options = {};
  if (options.repeated === undefined)
    options.repeated =
      !options.animate &&
      !options.oneStep &&
      testSolved() &&
      !getCells().every((a) => a.given);

  if (!options.oneStep || !untaintedFromLastStep) {
    clearConsole();
    resetKnownPuzzleInformation(true);
  }

  possible = true;
  solveOutput = null;

  if (!options.repeated) {
    if (!options.oneStep || !untaintedFromLastStep) {
      clearGrid(false, !boolSettings["Treat Pencil Marks as Given"]);
      resetKnownPuzzleInformation();
    }

    if (!testValid()) {
      solveOutput = "Invalid";
      log(formatSolveOutcome(solveOutput));
      disableInputs = false;
      changeUndo = true;
      return;
    } else if (
      !options.bruteForce &&
      (options.logicOnly || boolSettings["Attempt Logic Before Brute Force"])
    )
      logicalSolve({
        logProgress:
          options.logProgress === undefined
            ? options.logicOnly
            : options.logProgress,
        animate: options.animate,
        difficultyLimit: options.difficultyLimit,
        oneStep: options.oneStep,
      });
  } else resetKnownPuzzleInformation();

  if (!options.animate) stop = true;
  var wait = function () {
    if (!stop) setTimeout(wait, 1);
    else {
      if (!possible) {
        solveOutput = "Impossible";
        if (!options.logicOnly) clearConsole();
      }

      if (!solveOutput) {
        if (!options.logicOnly) {
          if (!options.repeated && testSolved()) solveOutput = "Solved";
          else solveOutput = bruteForce(options);
        } else solveOutput = testSolved() ? "Solved" : "Done";
      }

      if (!options.logicOnly && !["Solved", "Done"].includes(solveOutput)) {
        clearGrid();
        changeUndo = true;
      }

      if (!(options.oneStep && solveOutput === "Done" && changed))
        log(formatSolveOutcome(solveOutput));

      if (testSolved()) {
        puzzleTimer.pause();
        finished = true;
      }

      if (!options.dontEnableInputs) {
        disableInputs = false;
        if (options.animate) {
          setTimeout(function () {
            onInputEnd();
          }, 1);
        }
      }
    }
  };

  wait();
};

logicalSolve = function (options) {
  if (!options) options = {};

  if (
    (options.animate || options.oneStep) &&
    boolSettings["Display Candidates During Logic"]
  )
    showCandidates();

  if (isObviouslyImpossible()) {
    possible = false;
    stop = true;
    return "Impossible";
  }

  const solveStep = function () {
    changed = step({
      logProgress: options.logProgress,
      animate: options.animate,
      oneStep: options.oneStep,
      difficultyLimit: options.difficultyLimit,
    });

    if (testSolved() || !changed || !possible) {
      clearInterval(stepLoop);
      stop = true;
    }
  };

  changed = false;
  possible = true;
  stop = false;
  if (options.animate)
    var stepLoop = setInterval(solveStep, minStepDelay * 1000);
  else
    do {
      solveStep();
    } while (!stop && !options.oneStep);
};

step = function (options) {
  if (!options) options = {};

  changed = tryTechniques({
    logProgress:
      options.logProgress !== undefined ? options.logProgress : false,
    difficultyLimit:
      options.difficultyLimit || (options.bruteForce ? 1 : Infinity),
  });
  while (removeImpossibleCandidates(options.bruteForce)) changed = true;

  reduceLockedSets();

  if (!options.bruteForce) {
    if (
      (options.animate || options.oneStep) &&
      boolSettings["Display Candidates During Logic"]
    )
      showCandidates();

    if (isObviouslyImpossible()) possible = false;

    untaintedFromLastStep = true;
  }

  return changed;
};

resetKnownPuzzleInformation = function (beforeSolver) {
  //bruteForceGridStates = [];
  //bruteForceLockedSetsStates = [];

  if (!beforeSolver) {
    getSetTypes();

    lockedSets = [];
    for (var setType = 0; setType < setTypes.length; setType++) {
      for (
        var setIndex = 0;
        setIndex < numberOfSetsOfType(setTypes[setType]);
        setIndex++
      ) {
        const currentSet = getEmptyCellsInSet(setType, setIndex);

        for (var digit = 1; digit <= digits.length; digit++) {
          if (
            !getCellsInSet(setType, setIndex).some((a) => a.value === digit)
          ) {
            var lockedSet = currentSet.filter((a) =>
              a.candidates.includes(digit)
            );
            createLockedSet(
              digit,
              lockedSet,
              formatSet(setType, setIndex),
              false
            );
          }
        }
      }
    }

    constraint = constraints[cID("Killer Cage")];
    for (var a = 0; a < constraint.length; a++) {
      constraint[a].sums = [];
      if (constraint[a].value.length)
        constraint[a].sums = [
          ...sums[parseInt(constraint[a].value)][constraint[a].cells.length],
        ];
    }

    constraint = constraints[cID("Between Line")];
    for (var a = 0; a < constraint.length; a++) {
      constraint[a].minCell = null;
      constraint[a].maxCell = null;
    }

    constraint = constraints[cID("Quadruple")];
    for (var a = 0; a < constraint.length; a++) {
      if (constraint[a].values.length === 4)
        constraint[a].cells.forEach(
          (b) =>
            (b.candidates = b.candidates.filter((c) =>
              constraint[a].values.includes(c)
            ))
        );

      const values = new Set(constraint[a].values);
      values.forEach((b) => {
        if (
          constraint[a].values.indexOf(b) ===
          constraint[a].values.lastIndexOf(b)
        )
          createLockedSet(
            b,
            constraint[a].cells,
            "the " +
              constraint[a].values.join("") +
              " quadruple at " +
              formatCell(constraint[a].cells[0]),
            true,
            false
          );
        else {
          createLockedSet(
            b,
            [constraint[a].cells[0], constraint[a].cells[1]],
            "the " +
              constraint[a].values.join("") +
              " quadruple at " +
              formatCell(constraint[a].cells[0]),
            true,
            false
          );
          createLockedSet(
            b,
            [constraint[a].cells[1], constraint[a].cells[3]],
            "the " +
              constraint[a].values.join("") +
              " quadruple at " +
              formatCell(constraint[a].cells[0]),
            true,
            false
          );
          createLockedSet(
            b,
            [constraint[a].cells[2], constraint[a].cells[3]],
            "the " +
              constraint[a].values.join("") +
              " quadruple at " +
              formatCell(constraint[a].cells[0]),
            true,
            false
          );
          createLockedSet(
            b,
            [constraint[a].cells[0], constraint[a].cells[2]],
            "the " +
              constraint[a].values.join("") +
              " quadruple at " +
              formatCell(constraint[a].cells[0]),
            true,
            false
          );
        }
      });
    }

    reduceLockedSets();
  }

  constraint = constraints[cID("Sandwich Sum")];
  for (var a = 0; a < constraint.length; a++) {
    constraint[a].sums = [];
    if (constraint[a].value.length)
      constraint[a].sums = [].concat
        .apply([], sums[parseInt(constraint[a].value)])
        .filter((b) => !b.includes(1) && !b.includes(size));
  }
};

removeImpossibleCandidates = function () {
  var changed = false;
  for (var i = 0; i < size; i++) {
    for (var j = 0; j < size; j++) {
      for (var a = grid[i][j].candidates.length - 1; a >= 0; a--) {
        if (
          (grid[i][j].value && grid[i][j].value !== grid[i][j].candidates[a]) ||
          !candidatePossibleInCell(grid[i][j].candidates[a], grid[i][j])
        ) {
          grid[i][j].candidates.splice(a, 1);

          changed = true;
        }
      }
    }
  }

  return changed;
};

createLockedSet = function (value, cells, location, logic, logProgress) {
  if (
    !lockedSets.some(
      (a) => a.value === value && a.cells.every((b) => cells.includes(b))
    )
  ) {
    lockedSets.push({ value, cells, location });

    if (logic)
      return removeCandidatesFromCellsSeenByPointingSets(
        lockedSets[lockedSets.length - 1],
        logProgress,
        true
      );
  }
  return false;
};

reduceLockedSets = function () {
  for (var a = lockedSets.length - 1; a >= 0; a--) {
    if (lockedSets[a].cells.some((b) => b.value === lockedSets[a].value))
      lockedSets.splice(a, 1);
    else
      lockedSets[a].cells = lockedSets[a].cells.filter(
        (b) => !b.value && b.candidates.includes(lockedSets[a].value)
      );
  }
};

bruteForce = function (options) {
  if (!options) options = {};

  if (
    options.repeated &&
    !bruteForceGridStates.length &&
    !bruteForceLockedSetsStates.length
  )
    options.repeated = false;
  if (!options.repeated) {
    while (removeImpossibleCandidates()) {}
    bruteForceGridStates = [];
    bruteForceLockedSetsStates = [];
  }

  var cells = getCells();
  //cells.sort((a, b) => a.candidates.length - b.candidates.length);

  if (options.random)
    cells.forEach((a) => a.candidates.sort(() => Math.random() - 0.5));

  if (options.repeated) undoBruteForceStep(cells);

  const timeStarted = new Date().getTime();
  while (true) {
    if (new Date().getTime() - timeStarted >= 1000 * bruteForceTimeLimit) {
      clearGrid();
      changeUndo = true;
      return "Cancelled";
    }

    var index = cells.findIndex((a) => !a.value);

    var solved = testSolved();
    if (index === -1 && solved) return "Solved";
    if ((index === -1 && !solved) || !cells[index].candidates.length) {
      cells = undoBruteForceStep(cells);
      if (!cells) {
        clearGrid();
        if (options.repeated) return "Done";
        else return "Impossible";
      } else continue;
    }

    bruteForceGridStates.push(
      cells.map((a) => ({ value: a.value, candidates: [...a.candidates] }))
    );
    bruteForceLockedSetsStates.push([
      ...lockedSets.map((a) => ({
        cells: [...a.cells],
        value: a.value,
        location: a.location,
      })),
    ]);

    cells[index].value = cells[index].candidates[0];
    if (
      !candidatePossibleInCell(cells[index].value, cells[index], {
        bruteForce: true,
      })
    ) {
      cells = undoBruteForceStep(cells);
      continue;
    }

    reduceCandidatesFromUpdatesToCell(cells[index]);
    //while(removeImpossibleCandidates()){}
    reduceLockedSets();
    while (step({ logProgress: false, bruteForce: true })) {}

    if (isObviouslyImpossible(true)) cells = undoBruteForceStep(cells);
  }
};

undoBruteForceStep = function (cells) {
  if (!bruteForceGridStates.length) return false;

  state = bruteForceGridStates.pop();
  cells.forEach((a, i) => {
    a.value = state[i].value;
    a.candidates = [...state[i].candidates];
  });

  state = bruteForceLockedSetsStates.pop();
  lockedSets = [
    ...state.map((a) => ({
      cells: [...a.cells],
      value: a.value,
      location: a.location,
    })),
  ];

  var index = cells.findIndex((a) => !a.value);
  if (index > -1) {
    cells[index].candidates.shift();
    cells[index].value = 0;

    return cells;
  } else return false;
};

isObviouslyImpossible = function (dontLog, bruteForce) {
  for (var i = 0; i < size; i++) {
    for (var j = 0; j < size; j++) {
      if (
        !grid[i][j].candidates.length ||
        (!bruteForce &&
          grid[i][j].candidates.every(
            (a) => !candidatePossibleInCell(a, grid[i][j])
          ))
      ) {
        const reason = formatCell(grid[i][j]) + " has no candidates";
        if (!dontLog) log(reason);
        return reason;
      }
    }
  }

  for (var a = 0; a < lockedSets.length; a++) {
    if (
      lockedSets[a].cells.every(
        (b) => !b.candidates.includes(lockedSets[a].value)
      )
    ) {
      const reason =
        "There's nowhere to place " +
        lockedSets[a].value +
        " in " +
        lockedSets[a].location;
      if (!dontLog) log(reason);
      return reason;
    }
  }

  return false;
};
