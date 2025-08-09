testValid = function () {
  for (var a = 0; a < size; a++) {
    if (![size, 0].includes(getCells().filter((b) => b.region === a).length))
      return false;
  }

  for (var a = 0; a < constraints[cID("Palindrome")].length; a++) {
    for (var b = 0; b < constraints[cID("Palindrome")][a].lines.length; b++) {
      for (
        var c = 0;
        c < constraints[cID("Palindrome")][a].lines[b].length / 2;
        c++
      ) {
        if (
          getCellsSeenByCell(
            constraints[cID("Palindrome")][a].lines[b][c]
          ).includes(
            constraints[cID("Palindrome")][a].lines[b][
              constraints[cID("Palindrome")][a].lines[b].length - c - 1
            ]
          )
        )
          return false;
      }
    }
  }

  for (var a = 0; a < constraints[cID("Sandwich Sum")].length; a++) {
    const currentSandwich = constraints[cID("Sandwich Sum")][a];
    if (
      constraints[cID("Sandwich Sum")].findIndex(
        (b) =>
          b !== currentSandwich &&
          ((b.cell.i >= 0 &&
            b.cell.i < size &&
            b.cell.i === currentSandwich.cell.i) ||
            (b.cell.j >= 0 &&
              b.cell.j < size &&
              b.cell.j === currentSandwich.cell.j)) &&
          b.value !== currentSandwich.value
      ) > -1
    )
      return false;
  }

  if (constraints[cID("Ratio")].some((a) => a.value == 1)) return false;

  for (var a = 0; a < constraints[cID("Clone")].length; a++) {
    for (var b = 0; b < constraints[cID("Clone")][a].cells.length / 2; b++) {
      if (
        getCellsSeenByCell(constraints[cID("Clone")][a].cells[b]).includes(
          constraints[cID("Clone")][a].cloneCells[b]
        )
      )
        return false;
    }
  }

  return getCells().every(
    (a) => candidatePossibleInCell(a.value, a, { bruteForce: true }) || !a.given
  );
};

testFilled = function () {
  return getCells().every((a) => a.value);
};

testSolved = function () {
  return getCells().every((a) =>
    candidatePossibleInCell(a.value, a, { bruteForce: true })
  );
};

testPaused = function () {
  return mode === "Solving" && puzzleTimer.paused && !finished;
};
