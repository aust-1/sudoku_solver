togglePreview = function (screenshot) {
  if (saveDarkMode === null) {
    if (!screenshot) previewMode = true;
    saveDarkMode = boolSettings["Dark Mode"];
    boolSettings["Dark Mode"] = false;
    updateDarkMode();
  } else {
    previewMode = false;
    boolSettings["Dark Mode"] = saveDarkMode;
    saveDarkMode = null;
    updateDarkMode();
  }
};

outsideConstraintsVisible = function () {
  return (
    (!previewMode &&
      outsideTools.includes(currentTool) &&
      (toolConstraints.includes(currentTool) ||
        (toolCosmetics.includes(currentTool) &&
          cosmeticPlaceMode === "Outside"))) ||
    outsideConstraints.some((a) => constraints[cID(a)].length) ||
    toolCosmetics.some((a) =>
      cosmetics[cID(a)].some((b) => b.cells && b.cells.some((c) => c.outside))
    )
  );
};

adjustedX = function (x) {
  return outsideConstraintsVisible()
    ? (x - (gridX + gridSL / 2)) / (gridSL / (gridSL + 2 * cellSL)) +
        (gridX + gridSL / 2)
    : x;
};

adjustedY = function (y) {
  return outsideConstraintsVisible()
    ? (y - (gridY + gridSL / 2)) / (gridSL / (gridSL + 2 * cellSL)) +
        (gridY + gridSL / 2)
    : y;
};

mouseInGrid = function () {
  return (
    mouseX > gridX &&
    mouseX < gridX + gridSL &&
    mouseY > gridY &&
    mouseY < gridY + gridSL
  );
};

updateHeldKeys = function (event) {
  shifting = event.shiftKey;
  controlling = event.ctrlKey || event.metaKey;
  alting = event.altKey;
};

cID = function (str) {
  return str.split(" ").join("").toLowerCase();
};

isValidHexC = function (string) {
  return /^#[0-9A-F]{6}$/i.test(string);
};

hexBrightness = function (string) {
  return (
    (parseInt(string.substring(1, 3), 16) +
      parseInt(string.substring(3, 5), 16) +
      parseInt(string.substring(5, 7), 16)) /
    (255 * 3)
  );
};

rgbToHex = function (rgb) {
  return (
    "#" +
    rgb
      .map((x) => {
        const hex = x.toString(16).toUpperCase();
        return hex.length === 1 ? "0" + hex : hex;
      })
      .join("")
  );
};

invertBrightnessFromHex = function (hex) {
  console.log(hex);
  const rgb = [
    parseInt(hex.slice(1, 3), 16),
    parseInt(hex.slice(3, 5), 16),
    parseInt(hex.slice(5, 7), 16),
  ];
  const brightness = (rgb[0] + rgb[1] + rgb[2]) / 3;
  const brightnessChange = 255 - brightness * 2;
  for (var a = 0; a < 3; a++) {
    rgb[a] = Math.round(rgb[a] + brightnessChange);
    if (rgb[a] < 0) rgb[a] = 0;
    if (rgb[a] > 255) rgb[a] = 255;
  }

  return rgbToHex(rgb);
};

getCells = function () {
  var cells = [];
  for (var i = 0; i < grid.length; i++) cells = cells.concat(grid[i]);

  return cells;
};

getEmptyCells = function () {
  return getCells().filter((a) => !a.value);
};

nextSubgroup = function (indices, groupSize, index) {
  if (index === undefined) index = indices.length - 1;

  indices[index]++;
  if (indices[index] >= groupSize - (indices.length - index - 1)) {
    nextSubgroup(indices, groupSize, index - 1);
    indices[index] = indices[index - 1] + 1;
  }
};

generateSums = function () {
  sums = [];
  for (var a = 0; a <= maxInNCells(size); a++) {
    sums.push([!a ? [[]] : []]);
    for (var b = 1; b <= size; b++) sums[a].push([]);
  }

  for (var groupSize = 1; groupSize <= size; groupSize++) {
    var nums = [];
    for (var a = 1; a <= groupSize; a++) nums.push(a);

    while (!isNaN(nums[0])) {
      sums[nums.reduce((a, b) => a + b)][groupSize].push([...nums]);

      nextSubgroup(nums, size + 1);
    }
  }
};

minInNCells = function (n) {
  return (n * (n + 1)) / 2;
};

maxInNCells = function (n) {
  return ((2 * size + 1) * n - Math.pow(n, 2)) / 2;
};

showRules = function () {
  if (mode === "Solving" && !cameraX && customRuleset.length) {
    document.getElementById("rules").style.display = "block";
    document.getElementById("rules").value = customRuleset;
  }
};
