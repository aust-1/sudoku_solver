countSolutions = function (options, simple) {
  if (!options) options = {};

  clearConsole();
  clearGrid(false, !boolSettings["Treat Pencil Marks as Given"], true);
  var count = 0;
  var iterations = 0;

  do {
    solve({
      ...options,
      ...{
        logicOnly: iterations === 0,
        bruteForce: iterations > 0,
        repeated: count > 0,
        dontEnableInputs: true,
      },
    });

    if (["Invalid", "Impossible"].includes(solveOutput)) {
      finishedCountingSolutions(formatSolveOutcome(solveOutput));
      if (solveOutput === "Invalid") return solveOutput;
      else return 0;
    } else if (["Cancelled"].includes(solveOutput)) {
      finishedCountingSolutions(formatSolveOutcome(solveOutput));
      log(
        "This puzzle has at least " +
          count +
          " solution" +
          (count === 1 ? "" : "s")
      );
      return solveOutput;
    } else if (solveOutput === "Solved") count++;

    if (solveOutput === (iterations > 0 ? "Done" : "Solved")) {
      if (simple)
        finishedCountingSolutions("This puzzle has a unique solution");
      else
        finishedCountingSolutions(
          "This puzzle has " + count + " solution" + (count === 1 ? "" : "s")
        );
      return count;
    }

    if (simple) {
      if (count > 1) {
        finishedCountingSolutions("This puzzle has multiple solutions");
        return Infinity;
      }
    } else if (count >= solutionCountLimit) {
      finishedCountingSolutions(
        "This puzzle has at least " + solutionCountLimit + " solutions"
      );
      return solutionCountLimit;
    }

    iterations++;
  } while (true);
};

finishedCountingSolutions = function (output) {
  clearGrid();
  clearConsole();
  log(output);
  disableInputs = false;
  changeUndo = true;
};

rateDifficulty = function () {
  difficulty = 1;

  clearGrid();
  solve();

  changeUndo = true;
  onInputEnd(); // Remove if a button is added

  return difficulty;
};
