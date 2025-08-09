getSetTypes = function () {
  setTypes = ["Box", "Row", "Column"];

  if (constraints[cID("Extra Region")].length) setTypes.push("Extra Region");

  if (constraints[cID("Diagonal +")]) setTypes.push("Diagonal +");
  if (constraints[cID("Diagonal -")]) setTypes.push("Diagonal -");

  if (constraints[cID("Disjoint Groups")]) setTypes.push("Disjoint Group");
};

numberOfSetsOfType = function (type) {
  if (["Box"].includes(type))
    return new Set(
      getCells()
        .map((a) => a.region)
        .filter((a) => a !== null)
    ).size;

  if (["Row", "Column", "Disjoint Group"].includes(type)) return size;

  if (["Diagonal +", "Diagonal -"].includes(type)) return 1;

  if (["Extra Region"].includes(type))
    return constraints[cID("Extra Region")].length;

  return 0;
};

getEmptyCellsInSet = function (type, num) {
  return getCellsInSet(type, num).filter((a) => !a.value);
};

getCellsInSet = function (type, num) {
  if (setTypes[type] === "Box") return getCellsInRegion(num);
  if (setTypes[type] === "Row") return getCellsInRow(num);
  if (setTypes[type] === "Column") return getCellsInColumn(num);
  if (setTypes[type] === "Diagonal +") return getCellsInPDiagonal();
  if (setTypes[type] === "Diagonal -") return getCellsInNDiagonal();
  if (setTypes[type] === "Disjoint Group") return getCellsInDisjointGroup(num);
  if (setTypes[type] === "Extra Region") return getCellsInExtraRegion(num);
};

getCellsInRegion = function (num) {
  const cells = [];
  for (var i = 0; i < size; i++) {
    for (var j = 0; j < size; j++) {
      if (grid[i][j].region === num) cells.push(grid[i][j]);
    }
  }

  return cells;
};

getCellsInRow = function (num) {
  return grid[num];
};

getCellsInColumn = function (num) {
  const cells = [];
  for (var i = 0; i < size; i++) cells.push(grid[i][num]);

  return cells;
};

getCellsInPDiagonal = function () {
  const cells = [];
  for (var i = 0; i < size; i++) cells.push(grid[i][size - i - 1]);

  return cells;
};

getCellsInNDiagonal = function () {
  const cells = [];
  for (var i = 0; i < size; i++) cells.push(grid[i][i]);

  return cells;
};

getCellsInDisjointGroup = function (num) {
  const cells = [];
  for (var i = Math.floor(num / regionW); i < size; i += regionH) {
    for (var j = num % regionW; j < size; j += regionW) cells.push(grid[i][j]);
  }

  return cells;
};

getCellsInExtraRegion = function (num) {
  return [...constraints[cID("Extra Region")][num].cells];
};
