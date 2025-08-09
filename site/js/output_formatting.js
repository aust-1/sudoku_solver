unformatCell = function (cell) {
  const i = parseInt(cell.substring(1, cell.indexOf("C"))) - 1;
  const j = parseInt(cell.substring(cell.indexOf("C") + 1, cell.length)) - 1;
  if (i >= 0 && i < size && j >= 0 && j < size) return grid[i][j];
  else return outsideGrid[outsideGrid.findIndex((a) => a.i === i && a.j === j)];
};

formatCell = function (cell) {
  return "R" + (cell.i + 1) + "C" + (cell.j + 1);
};

formatCells = function (arr) {
  return listFromArray(
    arr
      .sort((a, b) => a.j - b.j)
      .sort((a, b) => a.i - b.i)
      .map((a) => formatCell(a)),
    "and"
  );
};

listFromArray = function (array, finalSeparator) {
  if (array.length > 1)
    return (
      array.slice(0, array.length - 1).join(", ") +
      " " +
      finalSeparator +
      " " +
      array[array.length - 1]
    );
  else return array[0];
};

uple = function (amount) {
  return upleNames[amount].toLowerCase();
};

number = function (num) {
  return numNames[num].toLowerCase();
};

formatSet = function (type, index) {
  if (["Box", "Row", "Column"].includes(setTypes[type]))
    return setTypes[type].toLowerCase() + " " + (index + 1);

  if (setTypes[type] === "Diagonal +") return "the positive diagonal";
  if (setTypes[type] === "Diagonal -") return "the negative diagonal";

  if (setTypes[type] === "Disjoint Group") return "group " + (index + 1);

  if (setTypes[type] === "Extra Region")
    return (
      "the extra region at " +
      formatCell(constraints[cID("Extra Region")][index].cells[0])
    );
};

formatSolveOutcome = function (outcome) {
  if (outcome === "Invalid") return "This is an invalid puzzle";
  if (outcome === "Impossible") return "This puzzle has no solutions";
  if (outcome === "Solved") return "Solved";
  if (outcome === "Done") return "No logical steps found";
  if (outcome === "Cancelled")
    return bruteForceTimeLimit + " second time limit reached; Solver cancelled";
};
