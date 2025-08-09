tryTechniques = function (options) {
  if (!options) options = {};

  // * = Classic sudoku technique

  // Naked singles *

  var placedDigit = false;
  for (var i = 0; i < grid.length; i++) {
    for (var j = 0; j < grid[i].length; j++) {
      const cell = grid[i][j];

      if (!cell.value && cell.candidates.length === 1) {
        if (options.logProgress)
          log(
            "Naked single;  " + formatCell(cell) + " → " + cell.candidates[0]
          );

        enter(cell.candidates[0], cell, options.logProgress);
        reduceCandidatesFromUpdatesToCell(cell);

        return true;
      }
    }
  }

  // Hidden singles *

  for (var a = 0; a < lockedSets.length; a++) {
    if (lockedSets[a].cells.length === 1) {
      if (options.logProgress)
        log(
          "Hidden single in " +
            lockedSets[a].location +
            ";  " +
            formatCell(lockedSets[a].cells[0]) +
            " → " +
            lockedSets[a].value
        );

      enter(lockedSets[a].value, lockedSets[a].cells[0], options.logProgress);
      reduceCandidatesFromUpdatesToCell(lockedSets[a].cells[0]);

      return true;
    }
  }

  if (2 > options.difficultyLimit) return false;
  difficulty = Math.max(2, difficulty);

  for (var groupSize = 2; groupSize <= size / 2; groupSize++) {
    // Naked pairs, triples, etc. *

    for (var setType = 0; setType < setTypes.length; setType++) {
      for (
        var setIndex = 0;
        setIndex < numberOfSetsOfType(setTypes[setType]);
        setIndex++
      ) {
        const currentSet = getEmptyCellsInSet(setType, setIndex);

        if (currentSet.length >= groupSize) {
          var indices = [];
          for (var a = 0; a < groupSize; a++) indices.push(a);

          while (!isNaN(indices[0])) {
            const allCandidatesInTheseCells = new Set();
            for (var a = 0; a < indices.length; a++) {
              for (var b = 0; b < currentSet[indices[a]].candidates.length; b++)
                allCandidatesInTheseCells.add(
                  currentSet[indices[a]].candidates[b]
                );
            }

            if (allCandidatesInTheseCells.size === groupSize) {
              const affected = getEmptyCellsSeenByCells(
                currentSet.filter((a) =>
                  indices.includes(currentSet.indexOf(a))
                )
              ).filter((a) =>
                Array.from(allCandidatesInTheseCells).some((b) =>
                  a.candidates.includes(b)
                )
              );

              if (affected.length) {
                if (options.logProgress)
                  log(
                    "Naked " +
                      uple(groupSize) +
                      " in " +
                      formatSet(setType, setIndex) +
                      ": " +
                      formatCells(
                        currentSet.filter((a) =>
                          indices.includes(currentSet.indexOf(a))
                        )
                      ) +
                      ";  " +
                      listFromArray(
                        Array.from(allCandidatesInTheseCells).sort(),
                        "and"
                      ) +
                      " removed as candidates from " +
                      formatCells(affected)
                  );

                allCandidatesInTheseCells.forEach((candidate) => {
                  for (var a = 0; a < affected.length; a++) {
                    if (affected[a].candidates.includes(candidate))
                      affected[a].candidates.splice(
                        affected[a].candidates.indexOf(candidate),
                        1
                      );
                  }
                });

                return true;
              }
            } else if (allCandidatesInTheseCells.size < groupSize)
              return "Impossible";

            nextSubgroup(indices, currentSet.length);
          }
        }
      }
    }

    // Hidden pairs, triples, etc. *

    for (var setType = 0; setType < setTypes.length; setType++) {
      for (
        var setIndex = 0;
        setIndex < numberOfSetsOfType(setTypes[setType]);
        setIndex++
      ) {
        const currentSet = getEmptyCellsInSet(setType, setIndex);

        if (currentSet.length >= groupSize) {
          var candidates = [];
          for (var a = 1; a <= groupSize; a++) candidates.push(a);

          while (!isNaN(candidates[0])) {
            const allCellsWithTheseCandidates = new Set();
            for (
              var candidateIndex = 0;
              candidateIndex < candidates.length;
              candidateIndex++
            ) {
              for (var a = 0; a < currentSet.length; a++) {
                if (
                  currentSet[a].candidates.includes(candidates[candidateIndex])
                )
                  allCellsWithTheseCandidates.add(currentSet[a]);
              }
            }

            if (
              candidates.every((a) =>
                Array.from(allCellsWithTheseCandidates).some((b) =>
                  b.candidates.includes(a)
                )
              )
            ) {
              if (allCellsWithTheseCandidates.size === groupSize) {
                const affected = [];
                allCellsWithTheseCandidates.forEach((cell) => {
                  for (var a = cell.candidates.length - 1; a >= 0; a--) {
                    if (!candidates.includes(cell.candidates[a])) {
                      if (!affected.includes(cell)) affected.push(cell);
                    }
                  }
                });

                if (affected.length) {
                  if (options.logProgress)
                    log(
                      "Hidden " +
                        uple(groupSize) +
                        " in " +
                        formatSet(setType, setIndex) +
                        ": " +
                        formatCells(Array.from(allCellsWithTheseCandidates)) +
                        ";  Removed all candidates other than " +
                        listFromArray(candidates, "and") +
                        " from " +
                        formatCells(affected)
                    );

                  for (var a = 0; a < affected.length; a++)
                    affected[a].candidates = affected[a].candidates.filter(
                      (candidate) => candidates.includes(candidate)
                    );
                  var seen = getEmptyCellsSeenByCells(
                    Array.from(allCellsWithTheseCandidates)
                  );
                  seen = seen.filter((cell) => {
                    if (
                      cell.candidates.some((candidate) =>
                        candidates.includes(candidate)
                      )
                    ) {
                      cell.candidates = cell.candidates.filter(
                        (candidate) => !candidates.includes(candidate)
                      );
                      return true;
                    } else return false;
                  });

                  if (options.logProgress && seen.length)
                    log(
                      ";  " +
                        listFromArray(candidates, "and") +
                        " removed as candidates from " +
                        formatCells(seen),
                      { newLine: false }
                    );

                  return true;
                }
              } else if (allCellsWithTheseCandidates.size < groupSize)
                return "Impossible";
            }

            nextSubgroup(candidates, size + 1);
          }
        }
      }
    }
  }

  // Pointing pairs, triples, etc. *

  for (var a = 0; a < lockedSets.length; a++) {
    if (
      removeCandidatesFromCellsSeenByPointingSets(
        lockedSets[a],
        options.logProgress
      ).length
    )
      return true;
  }

  // Extremes candidate reduction

  for (var i = 0; i < size; i++) {
    for (var j = 0; j < size; j++) {
      if (
        constraints[cID("Minimum")].findIndex((a) => a.cell === grid[i][j]) >= 0
      ) {
        const max = Math.min(
          ...getCellsOrthogonalToAndIncludingCell(grid[i][j])
            .filter(
              (a) =>
                a !== grid[i][j] &&
                constraints[cID("Minimum")].findIndex((b) => b.cell === a) ===
                  -1
            )
            .map((a) => Math.max(...a.candidates))
        );
        if (grid[i][j].candidates.some((a) => a >= max)) {
          grid[i][j].candidates = grid[i][j].candidates.filter((a) => a < max);

          if (options.logProgress)
            log(
              formatCell(grid[i][j]) +
                " can be no greater than " +
                (max - 1) +
                "; Other candidates removed"
            );

          return true;
        }
      } else if (
        constraints[cID("Maximum")].findIndex((a) => a.cell === grid[i][j]) >= 0
      ) {
        const min = Math.max(
          ...getCellsOrthogonalToAndIncludingCell(grid[i][j])
            .filter(
              (a) =>
                a !== grid[i][j] &&
                constraints[cID("Maximum")].findIndex((b) => b.cell === a) ===
                  -1
            )
            .map((a) => Math.min(...a.candidates))
        );
        if (grid[i][j].candidates.some((a) => a <= min)) {
          grid[i][j].candidates = grid[i][j].candidates.filter((a) => a > min);

          if (options.logProgress)
            log(
              formatCell(grid[i][j]) +
                " can be no less than " +
                (min + 1) +
                "; Other candidates removed"
            );

          return true;
        }
      }
    }
  }

  // Pairwise difference candidate reduction

  for (var index = 0; index < constraints[cID("Difference")].length; index++) {
    const currentDifference = constraints[cID("Difference")][index];
    if (!currentDifference.cells.some((a) => a.value)) {
      var iterationsSinceLastReduction = 0;
      var reduced = false;
      var cell = 0;
      while (iterationsSinceLastReduction < 2) {
        const oppositeCell = (cell + 1) % 2;
        const removableCandidates = [];
        for (
          var a = 0;
          a < currentDifference.cells[cell].candidates.length;
          a++
        ) {
          if (
            !currentDifference.cells[oppositeCell].candidates.includes(
              currentDifference.cells[cell].candidates[a] -
                (parseInt(currentDifference.value) || 1)
            ) &&
            !currentDifference.cells[oppositeCell].candidates.includes(
              currentDifference.cells[cell].candidates[a] +
                (parseInt(currentDifference.value) || 1)
            )
          )
            removableCandidates.push(
              currentDifference.cells[cell].candidates[a]
            );
        }

        if (removableCandidates.length) {
          for (var a = 0; a < removableCandidates.length; a++)
            currentDifference.cells[cell].candidates.splice(
              currentDifference.cells[cell].candidates.indexOf(
                removableCandidates[a]
              ),
              1
            );

          if (options.logProgress)
            log(
              formatCell(currentDifference.cells[oppositeCell]) +
                " cannot form a difference of " +
                (parseInt(currentDifference.value) || 1) +
                " with " +
                listFromArray(removableCandidates, "or") +
                ";  Candidate" +
                (removableCandidates.length === 1 ? "" : "s") +
                " removed from " +
                formatCell(currentDifference.cells[cell])
            );

          reduced = true;
          iterationsSinceLastReduction = 0;
        }

        iterationsSinceLastReduction += 1;
        cell = (cell + 1) % 2;
      }

      if (reduced) return true;
    }
  }

  // Pairwise ratio candidate reduction

  for (var index = 0; index < constraints[cID("Ratio")].length; index++) {
    const currentRatio = constraints[cID("Ratio")][index];
    if (!currentRatio.cells.some((a) => a.value)) {
      var iterationsSinceLastReduction = 0;
      var reduced = false;
      var cell = 0;
      while (iterationsSinceLastReduction < 2) {
        const oppositeCell = (cell + 1) % 2;
        const removableCandidates = [];
        for (var a = 0; a < currentRatio.cells[cell].candidates.length; a++) {
          if (
            !currentRatio.cells[oppositeCell].candidates.includes(
              currentRatio.cells[cell].candidates[a] /
                (parseInt(currentRatio.value) || 2)
            ) &&
            !currentRatio.cells[oppositeCell].candidates.includes(
              currentRatio.cells[cell].candidates[a] *
                (parseInt(currentRatio.value) || 2)
            )
          )
            removableCandidates.push(currentRatio.cells[cell].candidates[a]);
        }

        if (removableCandidates.length) {
          for (var a = 0; a < removableCandidates.length; a++)
            currentRatio.cells[cell].candidates.splice(
              currentRatio.cells[cell].candidates.indexOf(
                removableCandidates[a]
              ),
              1
            );

          if (options.logProgress)
            log(
              formatCell(currentRatio.cells[oppositeCell]) +
                " cannot form a ratio of " +
                (parseInt(currentRatio.value) || 2) +
                " with " +
                listFromArray(removableCandidates, "or") +
                ";  Candidate" +
                (removableCandidates.length === 1 ? "" : "s") +
                " removed from " +
                formatCell(currentRatio.cells[cell])
            );

          reduced = true;
          iterationsSinceLastReduction = 0;
        }

        iterationsSinceLastReduction += 1;
        cell = (cell + 1) % 2;
      }

      if (reduced) return true;
    }
  }

  // XV candidate reduction

  for (var index = 0; index < constraints[cID("XV")].length; index++) {
    const currentXV = constraints[cID("XV")][index];
    if (currentXV.value.length && !currentXV.cells.some((a) => a.value)) {
      var iterationsSinceLastReduction = 0;
      var reduced = false;
      var cell = 0;
      while (iterationsSinceLastReduction < 2) {
        const oppositeCell = (cell + 1) % 2;
        const removableCandidates = [];
        for (var a = 0; a < currentXV.cells[cell].candidates.length; a++) {
          if (
            !currentXV.cells[oppositeCell].candidates.includes(
              (currentXV.value === "X" ? 10 : 5) -
                currentXV.cells[cell].candidates[a]
            )
          )
            removableCandidates.push(currentXV.cells[cell].candidates[a]);
        }

        if (removableCandidates.length) {
          for (var a = 0; a < removableCandidates.length; a++)
            currentXV.cells[cell].candidates.splice(
              currentXV.cells[cell].candidates.indexOf(removableCandidates[a]),
              1
            );

          if (options.logProgress)
            log(
              formatCell(currentXV.cells[oppositeCell]) +
                " cannot form a sum of " +
                (currentXV.value === "X" ? 10 : 5) +
                " with " +
                listFromArray(removableCandidates, "or") +
                ";  Candidate" +
                (removableCandidates.length === 1 ? "" : "s") +
                " removed from " +
                formatCell(currentXV.cells[cell])
            );

          reduced = true;
          iterationsSinceLastReduction = 0;
        }

        iterationsSinceLastReduction += 1;
        cell = (cell + 1) % 2;
      }

      if (reduced) return true;
    }
  }

  // Nonconsecutively pointing pairs, triples, etc.

  if (constraints[cID("Nonconsecutive")]) {
    for (var a = 0; a < lockedSets.length; a++) {
      const eliminatableDigits = [
        lockedSets[a].value - 1,
        lockedSets[a].value + 1,
      ].filter((b) => digits.includes(b));

      const setsOfCellsSeenByTheseCells = lockedSets[a].cells.map((b) =>
        getEmptyCellsOrthogonalToAndIncludingCell(b).filter(
          (c) =>
            b === c ||
            (constraints[cID("Difference")].findIndex(
              (d) =>
                ["", "1"].includes(d.value) &&
                d.cells.includes(b) &&
                d.cells.includes(c)
            ) === -1 &&
              constraints[cID("Ratio")].findIndex(
                (d) =>
                  ["", "2"].includes(d.value) &&
                  d.cells.includes(b) &&
                  d.cells.includes(c)
              ) === -1)
        )
      );

      var cellsSeenByTheseCells = new Set();
      setsOfCellsSeenByTheseCells[0].forEach((b) => {
        if (setsOfCellsSeenByTheseCells.every((c) => c.includes(b)))
          cellsSeenByTheseCells.add(b);
      });
      cellsSeenByTheseCells = [...cellsSeenByTheseCells];

      const affected = [];
      cellsSeenByTheseCells.forEach((cell) => {
        for (var b = 0; b < eliminatableDigits.length; b++) {
          if (cell.candidates.includes(eliminatableDigits[b])) {
            affected.push(cell);
            break;
          }
        }
      });

      if (affected.length) {
        affected.forEach((cell) => {
          for (var b = 0; b < eliminatableDigits.length; b++) {
            if (cell.candidates.includes(eliminatableDigits[b]))
              cell.candidates.splice(
                cell.candidates.indexOf(eliminatableDigits[b]),
                1
              );
          }
        });

        if (options.logProgress)
          log(
            "All cells in " +
              lockedSets[a].location +
              " with " +
              lockedSets[a].value +
              " as a candidate are or are orthogonal to " +
              formatCells(affected) +
              ";  " +
              listFromArray(eliminatableDigits, "and") +
              " removed as " +
              (eliminatableDigits.length === 1 ? "a candidate" : "candidates") +
              " from " +
              formatCells(affected) +
              " because of the nonconsecutive constraint"
          );

        return true;
      }
    }
  }

  // Disallowed ratio pointing pairs, triples, etc.

  if (constraints[cID("Ratio")].negative) {
    const disallowedRatios = [
      ...new Set(constraints[cID("Ratio")].map((a) => parseInt(a.value) || 2)),
    ];
    if (!constraints[cID("Ratio")].length && !disallowedRatios.includes(2))
      disallowedRatios.push(2);
    for (var a = 0; a < lockedSets.length; a++) {
      const eliminatableDigits = [];
      for (var b = 0; b < disallowedRatios.length; b++) {
        if (digits.includes(lockedSets[a].value / disallowedRatios[b]))
          eliminatableDigits.push(lockedSets[a].value / disallowedRatios[b]);
        if (digits.includes(lockedSets[a].value * disallowedRatios[b]))
          eliminatableDigits.push(lockedSets[a].value * disallowedRatios[b]);
      }

      const setsOfCellsSeenByTheseCells = lockedSets[a].cells.map((b) =>
        getEmptyCellsOrthogonalToAndIncludingCell(b).filter(
          (c) =>
            constraints[cID("Difference")].findIndex(
              (d) =>
                ["", "1"].includes(d.value) &&
                d.cells.includes(b) &&
                d.cells.includes(c)
            ) === -1 &&
            constraints[cID("Ratio")].findIndex(
              (d) =>
                disallowedRatios.concat([""]).includes(d.value) &&
                d.cells.includes(b) &&
                d.cells.includes(c)
            ) === -1
        )
      );
      var cellsSeenByTheseCells = new Set();
      setsOfCellsSeenByTheseCells[0].forEach((b) => {
        if (setsOfCellsSeenByTheseCells.every((c) => c.includes(b)))
          cellsSeenByTheseCells.add(b);
      });
      cellsSeenByTheseCells = [...cellsSeenByTheseCells];

      const affected = [];
      cellsSeenByTheseCells.forEach((cell) => {
        for (var b = 0; b < eliminatableDigits.length; b++) {
          if (cell.candidates.includes(eliminatableDigits[b])) {
            affected.push(cell);
            break;
          }
        }
      });

      if (affected.length) {
        affected.forEach((cell) => {
          for (var b = 0; b < eliminatableDigits.length; b++) {
            if (cell.candidates.includes(eliminatableDigits[b]))
              cell.candidates.splice(
                cell.candidates.indexOf(eliminatableDigits[b]),
                1
              );
          }
        });

        if (options.logProgress)
          log(
            "All cells in " +
              lockedSets[a].location +
              " with " +
              lockedSets[a].value +
              " as a candidate are or are orthogonal to " +
              formatCells(affected) +
              ";  " +
              listFromArray(eliminatableDigits, "and") +
              " removed as " +
              (eliminatableDigits.length === 1 ? "a candidate" : "candidates") +
              " from " +
              formatCells(affected) +
              " because of the negative ratio constraint"
          );

        return true;
      }
    }
  }

  // Negative XV pointing pairs, triples, etc.

  if (constraints[cID("XV")].negative) {
    for (var a = 0; a < lockedSets.length; a++) {
      const eliminatableDigits = [
        10 - lockedSets[a].value,
        5 - lockedSets[a].value,
      ].filter((b) => digits.includes(b) && b !== 5);

      const setsOfCellsSeenByTheseCells = lockedSets[a].cells.map((b) =>
        getEmptyCellsOrthogonalToAndIncludingCell(b).filter(
          (c) =>
            b === c ||
            constraints[cID("XV")].findIndex(
              (d) => d.cells.includes(b) && d.cells.includes(c)
            ) === -1
        )
      );

      var cellsSeenByTheseCells = new Set();
      setsOfCellsSeenByTheseCells[0].forEach((b) => {
        if (setsOfCellsSeenByTheseCells.every((c) => c.includes(b)))
          cellsSeenByTheseCells.add(b);
      });
      cellsSeenByTheseCells = [...cellsSeenByTheseCells];

      const affected = [];
      cellsSeenByTheseCells.forEach((cell) => {
        for (var b = 0; b < eliminatableDigits.length; b++) {
          if (cell.candidates.includes(eliminatableDigits[b])) {
            affected.push(cell);
            break;
          }
        }
      });

      if (affected.length) {
        affected.forEach((cell) => {
          for (var b = 0; b < eliminatableDigits.length; b++) {
            if (cell.candidates.includes(eliminatableDigits[b]))
              cell.candidates.splice(
                cell.candidates.indexOf(eliminatableDigits[b]),
                1
              );
          }
        });

        if (options.logProgress)
          log(
            "All cells in " +
              lockedSets[a].location +
              " with " +
              lockedSets[a].value +
              " as a candidate are or are orthogonal to " +
              formatCells(affected) +
              ";  " +
              listFromArray(eliminatableDigits, "and") +
              " removed as " +
              (eliminatableDigits.length === 1 ? "a candidate" : "candidates") +
              " from " +
              formatCells(affected) +
              " because of the negative XV constraint"
          );

        return true;
      }
    }
  }

  // Orthogonally pointing cells

  if (
    constraints[cID("Nonconsecutive")] ||
    constraints[cID("Ratio")].negative ||
    constraints[cID("XV")].negative
  ) {
    const cells = getEmptyCells();

    const disallowedRatios = [
      ...new Set(constraints[cID("Ratio")].map((a) => parseInt(a.value) || 2)),
    ];
    if (!constraints[cID("Ratio")].length && !disallowedRatios.includes(2))
      disallowedRatios.push(2);

    for (var a = 0; a < cells.length; a++) {
      const adjacent = getEmptyCellsOrthogonalToAndIncludingCell(
        cells[a]
      ).filter((b) => b !== cells[a]);
      const adjacentEliminatable = [];
      for (var b = 0; b < adjacent.length; b++) {
        adjacentEliminatable.push([]);
        for (var digit = 1; digit <= size; digit++) {
          if (adjacent[b].candidates.includes(digit)) {
            if (
              cells[a].candidates.every(
                (c) =>
                  c === digit ||
                  (constraints[cID("Nonconsecutive")] &&
                    constraints[cID("Difference")].findIndex(
                      (d) =>
                        d.cells.includes(cells[a]) &&
                        d.cells.includes(adjacent[b])
                    ) === -1 &&
                    constraints[cID("Ratio")].findIndex(
                      (d) =>
                        d.cells.includes(cells[a]) &&
                        d.cells.includes(adjacent[b])
                    ) === -1 &&
                    Math.abs(c - digit) === 1) ||
                  (constraints[cID("Ratio")].negative &&
                    constraints[cID("Difference")].findIndex(
                      (d) =>
                        d.cells.includes(cells[a]) &&
                        d.cells.includes(adjacent[b])
                    ) === -1 &&
                    constraints[cID("Ratio")].findIndex(
                      (d) =>
                        d.cells.includes(cells[a]) &&
                        d.cells.includes(adjacent[b])
                    ) === -1 &&
                    (disallowedRatios.includes(c / digit) ||
                      disallowedRatios.includes(digit / c))) ||
                  (constraints[cID("XV")].negative &&
                    constraints[cID("XV")].findIndex(
                      (d) =>
                        d.cells.includes(cells[a]) &&
                        d.cells.includes(adjacent[b])
                    ) === -1 &&
                    [5, 10].includes(c + digit))
              )
            )
              adjacentEliminatable[b].push(digit);
          }
        }
      }

      if (adjacentEliminatable.some((b) => b.length)) {
        for (var b = 0; b < adjacentEliminatable.length; b++) {
          for (var c = 0; c < adjacentEliminatable[b].length; c++)
            adjacent[b].candidates.splice(
              adjacent[b].candidates.indexOf(adjacentEliminatable[b][c]),
              1
            );
        }

        reasons = ["equal to"];
        if (constraints[cID("Nonconsecutive")])
          reasons.push("consecutive with");
        if (constraints[cID("Ratio")].negative)
          reasons.push("form a disallowed ratio with");
        if (constraints[cID("XV")].negative)
          reasons.push("incorrectly sum to 5 or 10 with");
        if (options.logProgress)
          log(
            "All candidates in " +
              formatCell(cells[a]) +
              " are " +
              listFromArray(reasons, "or") +
              " " +
              listFromArray(
                [...new Set([].concat.apply([], adjacentEliminatable))],
                "and"
              ) +
              ";  Candidates eliminated from surrounding cells accordingly"
          );

        return true;
      }
    }
  }

  // Removal of candidates not appearing in possible killer sums

  if (constraints[cID("Killer Cage")].filter((a) => a.value.length).length) {
    for (
      var cageIndex = 0;
      cageIndex < constraints[cID("Killer Cage")].length;
      cageIndex++
    ) {
      const cage = constraints[cID("Killer Cage")][cageIndex];
      if (cage.value.length) {
        if (
          cage.cells.some((a) =>
            a.candidates.some((b) => cage.sums.every((c) => !c.includes(b)))
          )
        ) {
          if (options.logProgress)
            log(
              'The "' +
                cage.value +
                '" cage at ' +
                formatCell(cage.cells[0]) +
                (cage.sums.length === 1 ? " must be " : " can be ") +
                listFromArray(
                  cage.sums.map((a) => "[" + a.join(", ") + "]"),
                  "or"
                ) +
                "; Candidates not appearing in " +
                (cage.sums.length === 1 ? "this set" : "these sets") +
                " removed"
            );

          for (var cell = 0; cell < cage.cells.length; cell++) {
            for (var a = cage.cells[cell].candidates.length - 1; a >= 0; a--) {
              if (
                cage.sums.every(
                  (b) => !b.includes(cage.cells[cell].candidates[a])
                )
              )
                cage.cells[cell].candidates.splice(a, 1);
            }
          }

          return true;
        }
      }
    }
  }

  // Killer sum possibility reduction from impossible candidates

  if (constraints[cID("Killer Cage")].filter((a) => a.value.length).length) {
    for (
      var cageIndex = 0;
      cageIndex < constraints[cID("Killer Cage")].length;
      cageIndex++
    ) {
      const cage = constraints[cID("Killer Cage")][cageIndex];
      if (cage.value.length) {
        digitsNotIncluded = [];
        for (var digit = 1; digit <= size; digit++) {
          if (
            cage.cells.every((a) => !a.candidates.includes(digit)) &&
            cage.sums.some((a) => a.includes(digit))
          )
            digitsNotIncluded.push(digit);
        }

        if (digitsNotIncluded.length) {
          if (options.logProgress)
            log(
              'The "' +
                cage.value +
                '" cage at ' +
                formatCell(cage.cells[0]) +
                " cannot include " +
                listFromArray(digitsNotIncluded, "or") +
                " and therefore is not " +
                listFromArray(
                  cage.sums
                    .filter((a) => a.some((b) => digitsNotIncluded.includes(b)))
                    .map((a) => "[" + a.join(", ") + "]"),
                  "or"
                )
            );

          for (var a = cage.sums.length - 1; a >= 0; a--) {
            if (cage.sums[a].some((b) => digitsNotIncluded.includes(b)))
              cage.sums.splice(a, 1);
          }

          return true;
        }
      }
    }
  }

  // Killer sum possibility reduction from locked sets

  if (constraints[cID("Killer Cage")].filter((a) => a.value.length).length) {
    for (var a = 0; a < lockedSets.length; a++) {
      for (
        var cageIndex = 0;
        cageIndex < constraints[cID("Killer Cage")].length;
        cageIndex++
      ) {
        const cage = constraints[cID("Killer Cage")][cageIndex];
        if (cage.value.length) {
          if (
            cage.sums.some((b) => !b.includes(lockedSets[a].value)) &&
            lockedSets[a].cells.every((b) => cage.cells.includes(b))
          ) {
            if (options.logProgress)
              log(
                "All cells in " +
                  lockedSets[a].location +
                  " with " +
                  lockedSets[a].value +
                  ' as a candidate are contained within the "' +
                  cage.value +
                  '" cage at ' +
                  formatCell(cage.cells[0]) +
                  ", so the cage must contain " +
                  lockedSets[a].value +
                  " and therefore is not " +
                  listFromArray(
                    cage.sums
                      .filter((b) => !b.includes(lockedSets[a].value))
                      .map((b) => "[" + b.join(", ") + "]"),
                    "or"
                  )
              );

            for (var b = cage.sums.length - 1; b >= 0; b--) {
              if (!cage.sums[b].includes(lockedSets[a].value))
                cage.sums.splice(b, 1);
            }

            return true;
          }
        }
      }
    }
  }

  // Creating locked sets from killer sum possibilities

  if (constraints[cID("Killer Cage")].filter((a) => a.value.length).length) {
    for (
      var cageIndex = 0;
      cageIndex < constraints[cID("Killer Cage")].length;
      cageIndex++
    ) {
      const cage = constraints[cID("Killer Cage")][cageIndex];
      if (cage.value.length) {
        newForcedCandidates = [];
        for (var digit = 1; digit <= size; digit++) {
          if (
            cage.cells.every((a) => a.value !== digit) &&
            cage.sums.every((a) => a.includes(digit)) &&
            !lockedSets.some(
              (a) =>
                a.value === digit &&
                a.cells.every((b) =>
                  cage.cells
                    .filter((b) => b.candidates.includes(digit))
                    .includes(b)
                )
            )
          )
            newForcedCandidates.push(digit);
        }

        if (newForcedCandidates.length) {
          if (options.logProgress)
            log(
              'To complete the "' +
                cage.value +
                '" cage at ' +
                formatCell(cage.cells[0]) +
                ", it must contain " +
                listFromArray(newForcedCandidates, "and")
            );

          var eliminated = false;
          for (var a = 0; a < newForcedCandidates.length; a++) {
            if (
              createLockedSet(
                newForcedCandidates[a],
                cage.cells.filter((b) =>
                  b.candidates.includes(newForcedCandidates[a])
                ),
                'the "' + cage.value + '" cage at ' + formatCell(cage.cells[0]),
                true,
                options.logProgress
              ).length
            )
              eliminated = true;
          }

          if (!eliminated) removeLastLog();
          return true;
        }
      }
    }
  }

  // Sandwich sum possibility reduction from sandwich size

  if (constraints[cID("Sandwich Sum")].filter((a) => a.value.length).length) {
    for (
      var sandwichIndex = 0;
      sandwichIndex < constraints[cID("Sandwich Sum")].length;
      sandwichIndex++
    ) {
      const sandwich = constraints[cID("Sandwich Sum")][sandwichIndex];
      if (sandwich.value.length) {
        const ends = sandwich.set
          .filter(
            (a) => a.candidates.includes(1) || a.candidates.includes(size)
          )
          .map((a) => sandwich.set.indexOf(a));
        var sizes = new Set();
        ends.forEach((a, b) =>
          ends.forEach((c, d) => {
            if (d > b) sizes.add(c - a - 1);
          })
        );
        sizes = Array.from(sizes)
          .sort()
          .filter((a) => sandwich.sums.some((b) => b.length === a));

        if (sandwich.sums.some((a) => !sizes.includes(a.length))) {
          if (options.logProgress)
            log(
              "The 1 and " +
                size +
                " in " +
                sandwich.location +
                " must have " +
                listFromArray(
                  sizes.map((a) => number(a)),
                  "or"
                ) +
                ' cells between them, so the "' +
                sandwich.value +
                '" sandwich cannot contain ' +
                listFromArray(
                  sandwich.sums
                    .filter((a) => !sizes.includes(a.length))
                    .map((a) => "[" + a.join(", ") + "]"),
                  "or"
                )
            );

          for (var a = sandwich.sums.length - 1; a >= 0; a--) {
            if (!sizes.includes(sandwich.sums[a].length))
              sandwich.sums.splice(a, 1);
          }

          return true;
        }
      }
    }
  }

  // Removal of candidates not appearing in possible sandwich sums

  if (constraints[cID("Sandwich Sum")].filter((a) => a.value.length).length) {
    for (
      var sandwichIndex = 0;
      sandwichIndex < constraints[cID("Sandwich Sum")].length;
      sandwichIndex++
    ) {
      const sandwich = constraints[cID("Sandwich Sum")][sandwichIndex];
      if (sandwich.value.length && sandwich.value > 0) {
        const ends = sandwich.set
          .filter(
            (a) => a.candidates.includes(1) || a.candidates.includes(size)
          )
          .map((a) => sandwich.set.indexOf(a));

        set = [];
        if (ends.length === 2)
          set = sandwich.set.slice(ends[0] + 1, ends[ends.length - 1]);
        else if (
          ends[ends.length - 1] - sandwich.sums[0].length - 1 <=
          ends[0] + sandwich.sums[0].length + 2
        )
          set = sandwich.set.slice(
            ends[ends.length - 1] - sandwich.sums[0].length - 1,
            ends[0] + sandwich.sums[0].length + 2
          );

        if (set.length) {
          if (
            set.some((a) =>
              a.candidates.some(
                (b) =>
                  ![1, size].includes(b) &&
                  sandwich.sums.every((c) => !c.includes(b))
              )
            )
          ) {
            if (options.logProgress)
              log(
                'The "' +
                  sandwich.value +
                  '" sandwich in ' +
                  sandwich.location +
                  (sandwich.sums.length === 1
                    ? " must consist of "
                    : " can consist of ") +
                  listFromArray(
                    sandwich.sums.map((a) => "[" + a.join(", ") + "]"),
                    "or"
                  ) +
                  "; Candidates not appearing in " +
                  (sandwich.sums.length === 1 ? "this set" : "these sets") +
                  " removed from the inside of the sandwich"
              );

            for (var cell = 0; cell < set.length; cell++) {
              for (var a = set[cell].candidates.length - 1; a >= 0; a--) {
                if (
                  sandwich.sums.every(
                    (b) =>
                      ![1, size].includes(set[cell].candidates[a]) &&
                      !b.includes(set[cell].candidates[a])
                  )
                )
                  set[cell].candidates.splice(a, 1);
              }
            }

            return true;
          }
        }
      }
    }
  }

  // Sandwich sum possibility reduction from impossible candidates

  if (constraints[cID("Sandwich Sum")].filter((a) => a.value.length).length) {
    for (
      var sandwichIndex = 0;
      sandwichIndex < constraints[cID("Sandwich Sum")].length;
      sandwichIndex++
    ) {
      const sandwich = constraints[cID("Sandwich Sum")][sandwichIndex];
      if (sandwich.value.length) {
        const ends = sandwich.set
          .filter(
            (a) => a.candidates.includes(1) || a.candidates.includes(size)
          )
          .map((a) => sandwich.set.indexOf(a));

        digitsNotIncluded = [];
        for (var digit = 2; digit < size; digit++) {
          if (
            sandwich.set
              .slice(ends[0] + 1, ends[ends.length - 1])
              .every((a) => !a.candidates.includes(digit)) &&
            sandwich.sums.some((a) => a.includes(digit))
          )
            digitsNotIncluded.push(digit);
        }

        if (digitsNotIncluded.length) {
          if (options.logProgress)
            log(
              'The "' +
                sandwich.value +
                '" sandwich in ' +
                sandwich.location +
                " cannot contain " +
                listFromArray(digitsNotIncluded, "or") +
                " and therefore cannot contain " +
                listFromArray(
                  sandwich.sums
                    .filter((a) => a.some((b) => digitsNotIncluded.includes(b)))
                    .map((a) => "[" + a.join(", ") + "]"),
                  "or"
                )
            );

          for (var a = sandwich.sums.length - 1; a >= 0; a--) {
            if (sandwich.sums[a].some((b) => digitsNotIncluded.includes(b)))
              sandwich.sums.splice(a, 1);
          }

          return true;
        }
      }
    }
  }

  // Sandwich sum possibility reduction from locked sets

  if (constraints[cID("Sandwich Sum")].filter((a) => a.value.length).length) {
    for (var a = 0; a < lockedSets.length; a++) {
      if (![1, size].includes(lockedSets[a].value)) {
        for (
          var sandwichIndex = 0;
          sandwichIndex < constraints[cID("Sandwich Sum")].length;
          sandwichIndex++
        ) {
          const sandwich = constraints[cID("Sandwich Sum")][sandwichIndex];
          if (sandwich.value.length) {
            const ends = sandwich.set
              .filter(
                (b) => b.candidates.includes(1) || b.candidates.includes(size)
              )
              .map((b) => sandwich.set.indexOf(b));

            set = [];
            if (ends.length === 2)
              set = sandwich.set.slice(ends[0] + 1, ends[ends.length - 1]);
            else if (
              ends[ends.length - 1] - sandwich.sums[0].length - 1 <=
              ends[0] + sandwich.sums[0].length + 2
            )
              set = sandwich.set.slice(
                ends[ends.length - 1] - sandwich.sums[0].length - 1,
                ends[0] + sandwich.sums[0].length + 2
              );

            if (
              sandwich.sums.some((b) => !b.includes(lockedSets[a].value)) &&
              lockedSets[a].cells.every((b) => set.includes(b))
            ) {
              if (options.logProgress)
                log(
                  "All cells in " +
                    lockedSets[a].location +
                    " with " +
                    lockedSets[a].value +
                    ' as a candidate are contained within the "' +
                    sandwich.value +
                    '" sandwich in ' +
                    sandwich.location +
                    ", so the sandwich must contain " +
                    lockedSets[a].value +
                    " and therefore cannot contain " +
                    listFromArray(
                      sandwich.sums
                        .filter((b) => !b.includes(lockedSets[a].value))
                        .map((b) => "[" + b.join(", ") + "]"),
                      "or"
                    )
                );

              for (var b = sandwich.sums.length - 1; b >= 0; b--) {
                if (!sandwich.sums[b].includes(lockedSets[a].value))
                  sandwich.sums.splice(b, 1);
              }

              return true;
            }
          }
        }
      }
    }
  }

  // Creating locked sets from sandwich sum possibilities

  if (constraints[cID("Sandwich Sum")].filter((a) => a.value.length).length) {
    for (
      var sandwichIndex = 0;
      sandwichIndex < constraints[cID("Sandwich Sum")].length;
      sandwichIndex++
    ) {
      const sandwich = constraints[cID("Sandwich Sum")][sandwichIndex];
      if (sandwich.value.length) {
        const ends = sandwich.set
          .filter(
            (b) => b.candidates.includes(1) || b.candidates.includes(size)
          )
          .map((b) => sandwich.set.indexOf(b));

        newForcedCandidates = [];
        for (var digit = 2; digit < size; digit++) {
          if (
            sandwich.set.every((a) => a.value !== digit) &&
            sandwich.sums.every((a) => a.includes(digit)) &&
            !lockedSets.some(
              (a) =>
                a.value === digit &&
                a.cells.every((b) =>
                  sandwich.set
                    .slice(ends[0] + 1, ends[ends.length - 1])
                    .filter((b) => b.candidates.includes(digit))
                    .includes(b)
                )
            )
          )
            newForcedCandidates.push(digit);
        }

        if (newForcedCandidates.length) {
          if (options.logProgress)
            log(
              'To complete the "' +
                sandwich.value +
                '" sandwich in ' +
                sandwich.location +
                ", it must contain " +
                listFromArray(newForcedCandidates, "and")
            );

          var eliminated = false;
          for (var a = 0; a < newForcedCandidates.length; a++) {
            if (
              createLockedSet(
                newForcedCandidates[a],
                sandwich.set
                  .slice(ends[0] + 1, ends[ends.length - 1])
                  .filter((b) => b.candidates.includes(newForcedCandidates[a])),
                'the "' + sandwich.value + '" sandwich in ' + sandwich.location,
                true,
                options.logProgress
              ).length
            )
              eliminated = true;
          }

          if (!eliminated) removeLastLog();
          return true;
        }
      }
    }
  }

  // Between line direction discovery

  for (var a = 0; a < constraints[cID("Between Line")].length; a++) {
    const currentBetweenLine = constraints[cID("Between Line")][a].lines[0];
    if (
      !constraints[cID("Between Line")][a].minCell &&
      !constraints[cID("Between Line")][a].maxCell
    ) {
      for (
        var index = 0, side = 0;
        side <= 1;
        index += currentBetweenLine.length - 1, side++
      ) {
        const oppositeIndex =
          (index + (currentBetweenLine.length - 1)) %
          (2 * (currentBetweenLine.length - 1));
        var foundDirection = false;
        for (var b = 1; b < currentBetweenLine.length - 1; b++) {
          if (
            Math.max(...currentBetweenLine[index].candidates) <=
              Math.min(...currentBetweenLine[b].candidates) ||
            Math.min(...currentBetweenLine[oppositeIndex].candidates) >=
              Math.max(...currentBetweenLine[b].candidates)
          ) {
            constraints[cID("Between Line")][a].minCell =
              currentBetweenLine[index];
            constraints[cID("Between Line")][a].maxCell =
              currentBetweenLine[oppositeIndex];
            foundDirection = true;
          } else if (
            Math.min(...currentBetweenLine[index].candidates) >=
              Math.max(...currentBetweenLine[b].candidates) ||
            Math.max(...currentBetweenLine[oppositeIndex].candidates) <=
              Math.min(...currentBetweenLine[b].candidates)
          ) {
            constraints[cID("Between Line")][a].minCell =
              currentBetweenLine[oppositeIndex];
            constraints[cID("Between Line")][a].maxCell =
              currentBetweenLine[index];
            foundDirection = true;
          }

          if (foundDirection) {
            for (var c = 1; c < currentBetweenLine.length - 1; c++)
              currentBetweenLine[c].candidates = currentBetweenLine[
                c
              ].candidates.filter(
                (d) =>
                  d >
                    Math.min(
                      ...constraints[cID("Between Line")][a].minCell.candidates
                    ) &&
                  d <
                    Math.max(
                      ...constraints[cID("Between Line")][a].maxCell.candidates
                    )
              );

            if (options.logProgress)
              log(
                "Because of " +
                  formatCell(currentBetweenLine[b]) +
                  ", " +
                  formatCell(constraints[cID("Between Line")][a].minCell) +
                  " must be the minimum and " +
                  formatCell(constraints[cID("Between Line")][a].maxCell) +
                  " the maximum of its between line; Candidates removed accordingly"
              );

            return true;
          }
        }
      }
    }
  }

  // Pointing pairs on ends of between lines

  for (var a = 0; a < constraints[cID("Between Line")].length; a++) {
    const currentBetweenLine = constraints[cID("Between Line")][a].lines[0];
    const end1 = currentBetweenLine[0];
    const end2 = currentBetweenLine[currentBetweenLine.length - 1];
    const min = Math.min(
      Math.min(...end1.candidates),
      Math.min(...end2.candidates)
    );
    const max = Math.max(
      Math.max(...end1.candidates),
      Math.max(...end2.candidates)
    );

    if (!end1.value && !end2.value) {
      for (var mm = 0; mm < 2; mm++) {
        if (
          currentBetweenLine
            .slice(1, currentBetweenLine.length - 1)
            .some((b) => b.value === (!mm ? min + 1 : max - 1))
        ) {
          outcome = createLockedSet(
            !mm ? min : max,
            [end1, end2],
            "the ends of the between line from " +
              formatCell(end1) +
              " to " +
              formatCell(end2),
            true
          );

          if (outcome) {
            if (outcome.length && options.logProgress)
              log(
                "The ends of the between line from " +
                  formatCell(end1) +
                  " to " +
                  formatCell(end2) +
                  " must contain " +
                  (!mm ? min : max) +
                  " because of their shared " +
                  (!mm ? "minimum" : "maximum") +
                  " and the presence of a " +
                  (!mm ? min + 1 : max - 1) +
                  " on the line; " +
                  (!mm ? min : max) +
                  " removed as a candidate from " +
                  formatCells(outcome)
              );

            return true;
          }
        }
      }
    }
  }

  if (3 > options.difficultyLimit) return false;
  difficulty = Math.max(3, difficulty);

  // X-Wings, swordfish, etc. *

  for (var groupSize = 2; groupSize <= size / 2; groupSize++) {
    for (var setType = 1; setType < 3; setType++) {
      for (var digit = 1; digit <= size; digit++) {
        var indices = [];
        for (var setIndex = 0; setIndex < groupSize; setIndex++)
          indices.push(setIndex);

        while (!isNaN(indices[0])) {
          var currentSets = [];
          for (var a = 0; a < groupSize; a++)
            currentSets.push(getEmptyCellsInSet(setType, indices[a]));

          if (
            currentSets.every((a) =>
              a.some((b) => b.candidates.includes(digit))
            )
          ) {
            var allSetsInTheseCells = new Set();
            for (var a = 0; a < groupSize; a++) {
              for (var b = 0; b < currentSets[a].length; b++) {
                if (currentSets[a][b].candidates.includes(digit)) {
                  if (setType === 1)
                    allSetsInTheseCells.add(currentSets[a][b].j);
                  if (setType === 2)
                    allSetsInTheseCells.add(currentSets[a][b].i);
                }
              }
            }

            if (allSetsInTheseCells.size === groupSize) {
              const affected = [];
              allSetsInTheseCells = Array.from(allSetsInTheseCells);
              for (var a = 0; a < allSetsInTheseCells.length; a++) {
                const intersectingSet = getEmptyCellsInSet(
                  setType === 1 ? 2 : 1,
                  allSetsInTheseCells[a]
                );

                for (var b = 0; b < intersectingSet.length; b++) {
                  if (
                    (setType === 1 &&
                      !indices.includes(intersectingSet[b].i)) ||
                    (setType === 2 && !indices.includes(intersectingSet[b].j))
                  ) {
                    if (intersectingSet[b].candidates.includes(digit))
                      affected.push(intersectingSet[b]);
                  }
                }
              }

              if (affected.length) {
                for (var a = 0; a < affected.length; a++)
                  affected[a].candidates.splice(
                    affected[a].candidates.indexOf(digit),
                    1
                  );

                if (options.logProgress)
                  log(
                    fishNames[groupSize] +
                      " on " +
                      digit +
                      "s in " +
                      (setType === 1 ? "rows " : "columns ") +
                      listFromArray(
                        indices.map((a) => a + 1),
                        "and"
                      ) +
                      ";  " +
                      digit +
                      " removed as a candidate from " +
                      formatCells(affected)
                  );

                return true;
              }
            }
          }

          nextSubgroup(indices, size);
        }
      }
    }
  }

  // Y-Wing *

  const bivalueCells = getCells().filter((a) => a.candidates.length === 2);
  for (var a = 0; a < bivalueCells.length; a++) {
    const cellOptions = getCellsSeenByCell(bivalueCells[a]).filter(
      (b) =>
        bivalueCells.includes(b) &&
        new Set([...bivalueCells[a].candidates, ...b.candidates]).size === 3
    );
    if (cellOptions.length >= 2) {
      var indices = [0, 1];
      while (!isNaN(indices[0])) {
        if (
          new Set([
            ...cellOptions[indices[0]].candidates,
            ...cellOptions[indices[1]].candidates,
          ]).size === 3
        ) {
          var digit =
            cellOptions[indices[0]].candidates[
              cellOptions[indices[0]].candidates.findIndex(
                (b) =>
                  cellOptions[indices[1]].candidates.includes(b) &&
                  !bivalueCells[a].candidates.includes(b)
              )
            ];
          if (digit) {
            const affected = getEmptyCellsSeenByCells([
              cellOptions[indices[0]],
              cellOptions[indices[1]],
            ]).filter((b) => b.candidates.includes(digit));
            if (affected.length) {
              for (var b = 0; b < affected.length; b++)
                affected[b].candidates.splice(
                  affected[b].candidates.indexOf(digit),
                  1
                );

              if (options.logProgress)
                log(
                  "Y-Wing hinged at " +
                    formatCell(bivalueCells[a]) +
                    " on " +
                    formatCells(indices.map((b) => cellOptions[b])) +
                    ";  " +
                    digit +
                    " removed as a candidate from " +
                    formatCells(affected)
                );

              return true;
            }
          }
        }

        nextSubgroup(indices, cellOptions.length);
      }
    }
  }

  // Skyscraper *

  for (var setType = 1; setType < 3; setType++) {
    for (var digit = 1; digit <= size; digit++) {
      var indices = [];
      for (var setIndex = 0; setIndex < 2; setIndex++) indices.push(setIndex);

      while (!isNaN(indices[0])) {
        var currentSets = [];
        for (var a = 0; a < 2; a++)
          currentSets.push(getEmptyCellsInSet(setType, indices[a]));

        if (
          currentSets.every(
            (a) => a.filter((b) => b.candidates.includes(digit)).length === 2
          )
        ) {
          var allSetsInTheseCells = new Set();
          var affecting = [];
          for (var a = 0; a < 2; a++) {
            for (var b = 0; b < currentSets[a].length; b++) {
              if (currentSets[a][b].candidates.includes(digit)) {
                if (setType === 1) allSetsInTheseCells.add(currentSets[a][b].j);
                if (setType === 2) allSetsInTheseCells.add(currentSets[a][b].i);
                affecting.push(currentSets[a][b]);
              }
            }
          }

          if (allSetsInTheseCells.size === 3) {
            affecting = affecting.filter(
              (a) =>
                affecting.findIndex((b) =>
                  setType === 1 ? a.j === b.j : a.i === b.i
                ) ===
                affecting.length -
                  [...affecting]
                    .reverse()
                    .findIndex((b) =>
                      setType === 1 ? a.j === b.j : a.i === b.i
                    ) -
                  1
            );
            const affected = getEmptyCellsSeenByCells(affecting).filter((a) =>
              a.candidates.includes(digit)
            );

            if (affected.length) {
              for (var a = 0; a < affected.length; a++)
                affected[a].candidates.splice(
                  affected[a].candidates.indexOf(digit),
                  1
                );

              if (options.logProgress)
                log(
                  "Skyscraper on " +
                    digit +
                    "s in " +
                    (setType === 1 ? "rows " : "columns ") +
                    listFromArray(
                      indices.map((a) => a + 1),
                      "and"
                    ) +
                    ";  " +
                    digit +
                    " removed as a candidate from " +
                    formatCells(affected)
                );

              return true;
            }
          }
        }

        nextSubgroup(indices, size);
      }
    }
  }

  // Unorthodox naked pairs, triples, etc.

  if (
    (constraints[cID("Diagonal +")] && constraints[cID("Diagonal -")]) ||
    constraints[cID("Antiknight")] ||
    constraints[cID("Antiking")] ||
    constraints[cID("Extra Region")] ||
    constraints[cID("Killer Cage")].length
  ) {
    for (var groupSize = 2; groupSize <= size / 2; groupSize++) {
      const currentSet = getEmptyCells().filter(
        (a) => a.candidates.length <= groupSize
      );
      if (currentSet.length >= groupSize) {
        var indices = [];
        for (var a = 0; a < groupSize; a++) indices.push(a);

        while (!isNaN(indices[0])) {
          const cellsInGroup = [];
          for (var a = 0; a < indices.length; a++)
            cellsInGroup.push(currentSet[indices[a]]);

          if (
            cellsInGroup.every((a) => {
              const seen = getEmptyCellsSeenByCell(a);
              return cellsInGroup.every((b) => a === b || seen.includes(b));
            })
          ) {
            const allCandidatesInTheseCells = new Set();
            for (var a = 0; a < indices.length; a++) {
              for (var b = 0; b < currentSet[indices[a]].candidates.length; b++)
                allCandidatesInTheseCells.add(
                  currentSet[indices[a]].candidates[b]
                );
            }

            if (allCandidatesInTheseCells.size === groupSize) {
              const affected = getEmptyCellsSeenByCells(
                currentSet.filter((a) =>
                  indices.includes(currentSet.indexOf(a))
                )
              ).filter((a) =>
                Array.from(allCandidatesInTheseCells).some((b) =>
                  a.candidates.includes(b)
                )
              );

              if (affected.length) {
                if (options.logProgress)
                  log(
                    "Unorthodox naked " +
                      uple(groupSize) +
                      ": " +
                      formatCells(
                        currentSet.filter((a) =>
                          indices.includes(currentSet.indexOf(a))
                        )
                      ) +
                      ";  " +
                      listFromArray(
                        Array.from(allCandidatesInTheseCells).sort(),
                        "and"
                      ) +
                      " removed as candidates from " +
                      formatCells(affected)
                  );

                allCandidatesInTheseCells.forEach((candidate) => {
                  for (var a = 0; a < affected.length; a++) {
                    if (affected[a].candidates.includes(candidate))
                      affected[a].candidates.splice(
                        affected[a].candidates.indexOf(candidate),
                        1
                      );
                  }
                });

                return true;
              }
            }
          }

          nextSubgroup(indices, currentSet.length);
        }
      }
    }
  }

  if (4 > options.difficultyLimit) return false;
  difficulty = Math.max(4, difficulty);

  // Chains of length 0 or 1 *

  const emptyCells = getEmptyCells().sort(
    (a, b) => a.candidates.length - b.candidates.length
  );
  emptyCells.forEach((a) => {
    a.valueBackup = a.value;
    a.candidatesBackup = [...a.candidates];
  });
  for (var cell = 0; cell < emptyCells.length; cell++) {
    for (
      var candidate = 0;
      candidate < emptyCells[cell].candidates.length;
      candidate++
    ) {
      emptyCells[cell].value = emptyCells[cell].candidates[candidate];
      emptyCells[cell].candidates = [emptyCells[cell].candidates[candidate]];

      var changedCells = [];
      for (var steps = 0; steps <= 1; steps++) {
        while (removeImpossibleCandidates()) {}

        const impossible = isObviouslyImpossible(true);
        if (impossible) {
          if (steps) {
            changedCellsBackup = [...changedCells];
            changedCells = changedCells.filter((b) => {
              emptyCells.forEach((c) => {
                c.candidates = [...c.candidatesBackup];
              });

              newValue = b.value;
              newCandidates = [...b.candidates];
              b.value = b.valueBackup;
              b.candidates = [...b.candidatesBackup];

              while (removeImpossibleCandidates()) {}
              const necessary = isObviouslyImpossible(true) !== impossible;

              b.value = newValue;
              b.candidates = [...newCandidates];
              return necessary;
            });

            if (!changedCells.length) changedCells = [...changedCellsBackup];
            changeList = listFromArray(
              changedCells
                .filter((b) => b.value)
                .map((b) => b.value + " into " + formatCell(b)),
              "and"
            );
          }

          emptyCells.forEach((b) => {
            b.value = b.valueBackup;
            b.candidates = [...b.candidatesBackup];
          });

          if (options.logProgress) {
            if (steps === 0)
              log(
                "Placing " +
                  emptyCells[cell].candidates[candidate] +
                  " in " +
                  formatCell(emptyCells[cell]) +
                  " causes a contradiction: " +
                  impossible +
                  "; Candidate removed."
              );
            if (steps === 1)
              log(
                "Placing " +
                  emptyCells[cell].candidates[candidate] +
                  " in " +
                  formatCell(emptyCells[cell]) +
                  " forces " +
                  changeList +
                  ", which causes a contradiction: " +
                  impossible +
                  "; Candidate removed."
              );
          }

          emptyCells[cell].candidates.splice(candidate, 1);

          return true;
        }

        for (var a = 0; a < emptyCells.length; a++) {
          if (!emptyCells[a].value && emptyCells[a].candidates.length === 1) {
            if (
              candidatePossibleInCell(
                emptyCells[a].candidates[0],
                emptyCells[a],
                { bruteForce: true }
              )
            )
              emptyCells[a].value = emptyCells[a].candidates[0];
            changedCells.push(emptyCells[a]);
          }
        }
      }

      emptyCells.forEach((a) => {
        a.value = a.valueBackup;
        a.candidates = [...a.candidatesBackup];
      });
    }
  }

  if (5 > options.difficultyLimit) return false;
  difficulty = Math.max(5, difficulty);

  return false;
};

removeCandidatesFromCellsSeenByPointingSets = function (
  pointingSet,
  logProgress,
  creatingNew
) {
  const affected = getEmptyCellsSeenByCells(pointingSet.cells).filter((b) =>
    b.candidates.includes(pointingSet.value)
  );

  if (affected.length) {
    for (var b = 0; b < affected.length; b++)
      affected[b].candidates.splice(
        affected[b].candidates.indexOf(pointingSet.value),
        1
      );

    if (logProgress)
      log(
        (creatingNew
          ? ""
          : "Pointing " +
            uple(pointingSet.cells.length) +
            " in " +
            pointingSet.location +
            ": " +
            formatCells(pointingSet.cells)) +
          ";  " +
          pointingSet.value +
          " removed as a candidate from " +
          formatCells(affected),
        { newLine: !creatingNew }
      );
  }

  return affected;
};
