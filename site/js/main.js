const everything = document.getElementById("everything");
const canvas = document.getElementById("canvas1");
const canvas2 = document.getElementById("canvas2");
const canvas3 = document.getElementById("canvas3");
const consoleOutput = document.getElementById("console");
const cPicker = new iro.ColorPicker("#colorPicker", {
  borderColor: "#000000",
  layout: [{ component: iro.ui.Wheel }, { component: iro.ui.Slider }],
});

var ctx = canvas.getContext("2d");
ctx.textAlign = "center";

const version = "1.11.2";

var mobile = false;

const urlString = "?id=";
const importString = "?load=";

var loaded = false;

const titleLSize = 50; // Pixels tall
const titleSSize = 45; // Pixels tall
const maxTitleW = 0.8; // Times canvas.width
var customTitle = "";
var author = "";
var customRuleset = "";
var disableHC = false;

var mode = "Setting";
var enterMode = (tempEnterMode = "Normal");

var grid = [];
var outsideGrid = [];
const gridTopMargin = 100; // Pixels
const gridBottomMargin = 40; // Pixels
var gridX = null;
var gridY = null;
var gridSL = null;
var cellSL = null;

const lineWW = 5.5; // Pixels
const lineWT = 1.5; // Pixels

var sidebars = [];
const sidebarDist = 90; // Pixels from the edge of the grid
const sidebarGap = 40; // Pixels
const sidebarW = 300; // Pixels
const sidebarTitleHeight = 40; // Pixels
const buttonMargin = 15; // Pixels

const buttonW = sidebarW - buttonMargin * 2; // Pixels
const buttonLH = 45; // Pixels
const buttonSH = 32.1; // Pixels
const buttonGap = 10; // Pixels

var previewMode = false;
const downloadResolution = 2; // Times gridSL

var cameraX = 0;
const cameraMoveAmount = 350; // Pixels

var currentTool = null;
var lastTool = null;

const constraints = {};
const cosmetics = {};
const cosmeticPlaceModes = ["Auto", "Cell", "Border", "Corner", "Outside"];
var cosmeticPlaceMode = cosmeticPlaceModes[0];

var cosmeticEditMenuY = 0;
var cosmeticEditMenuH = 0;
const cPickerH = 225; // Pixels
const cosmeticEditMenuYOffset = 100; // Pixels
const cosmeticEditMenuCBoxGap = 30; // Pixels
const cosmeticEditMenuCloseForgiveness = 20; // Pixels

const cosmeticSizeStep = 0.05; // Cells
const cosmeticAngleStep = 15; // Degrees

const cosmeticMinSize = 0.25;
const cosmeticMaxSize = 1.5;
const cosmeticTypableCharacters =
  " ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890><=+-^_!?*~()[]{}\"'/|\\#%&".split("");

var dragAnchor = null;
var dragShift = false;
var dragMode = null;

var sums = [];

var output = "";

var size = (tempSize = 9); // Cells
var regionW = null;
var regionH = null;
var digits = [];
const sizes = {
  3: { w: 3, h: 1 },
  4: { w: 2, h: 2 },
  5: { w: 5, h: 1 },
  6: { w: 3, h: 2 },
  7: { w: 7, h: 1 },
  8: { w: 4, h: 2 },
  9: { w: 3, h: 3 },
  10: { w: 5, h: 2 },
  11: { w: 11, h: 1 },
  12: { w: 4, h: 3 },
  13: { w: 13, h: 1 },
  14: { w: 7, h: 2 },
  15: { w: 5, h: 3 },
  16: { w: 4, h: 4 },
};

var setTypes = [];
const numNames = [
  "",
  "One",
  "Two",
  "Three",
  "Four",
  "Five",
  "Six",
  "Seven",
  "Eight",
  "Nine",
  "Ten",
  "Eleven",
  "Twelve",
  "Thirteen",
  "Fourteen",
  "Fifteen",
  "Sixteen",
];
const upleNames = [
  "",
  "Single",
  "Pair",
  "Triple",
  "Quadruple",
  "Quintuple",
  "Sextuple",
  "Septuple",
  "Octuple",
  "Nonuple",
  "Decuple",
];
const fishNames = [
  "",
  "",
  "X-Wing",
  "Swordfish",
  "Jellyfish",
  "Squirmbag",
  "Whale",
  "Leviathan",
  "undefined",
];

var changes = [];
var changeIndex = 0;
var changeCancelled = false;
var changeUndo = false;

var selection = [];
var cellsSeenBySelection = [];

var highlightCs = [
  "#FFFFFF",
  "#A8A8A8",
  "#000000",
  "#FFA0A0",
  "#FFE060",
  "#FFFFB0",
  "#B0FFB0",
  "#60D060",
  "#D0D0FF",
  "#8080F0",
  "#FF80FF",
  "#FFD0D0",
];

const puzzleTimer = new timer();
var finished = false;

var confirmSolve = false;
var confirmClear = false;
var confirmClearTimer = false;

var popup = null;
const popups = {
  info: { w: 700, h: 570 },
  settings: { w: 600, h: 720 },
  newgrid: { w: 600, h: 250 },
  export: { w: 850, h: 500 },
  editinfo: { w: 660, h: 610 },
};

var bruteForceGridStates = [];
var bruteForceLockedSetsStates = [];

var untaintedFromLastStep = true;

var difficulty = 1;
var difficultyReached = false;

var lockedSets = [];

const symmetries = ["90", "180", "V", "H"];

addAllCandidates = function (cell) {
  var cells = cell ? [cell] : getCells();
  cells.forEach((a) => {
    a.candidates = [];

    for (var digit = 1; digit <= size; digit++) {
      if (!a.given || a.value === digit) a.candidates.push(digit);
    }
  });
};

generateCandidates = function () {
  addAllCandidates();
  if (boolSettings["Treat Pencil Marks as Given"]) {
    getCells().forEach((a) => {
      if (a.centerPencilMarks.length) a.candidates = [...a.centerPencilMarks];
    });
  }

  while (removeImpossibleCandidates()) {}

  untaintedFromLastStep = false;
};

showCandidates = function () {
  getCells().forEach((a) => (a.centerPencilMarks = [...a.candidates]));
};

setCurrentTool = function (id, keepEnterMode) {
  if (currentTool !== id) {
    lastTool = currentTool;
    currentTool = id;

    if (!selectableConstraints.includes(currentTool)) selection = [];

    if (!keepEnterMode) setEnterMode("Normal", true);
  }
};

setEnterMode = function (newMode, keepCurrentConstraint) {
  enterMode = newMode;
  if (currentTool !== "Given Digit" || (!shifting && !controlling))
    tempEnterMode = enterMode;

  if (!keepCurrentConstraint) setCurrentTool("Given Digit", true);
  createSidebars();
};

enter = function (num, cell, logProgress) {
  if (!cell) {
    bruteForceGridStates = [];
    bruteForceLockedSetsStates = [];
  }

  if (
    mode === "Solving" ||
    selectableConstraints.includes(currentTool) ||
    cell
  ) {
    if (
      !cell &&
      tempEnterMode === "Highlight" &&
      !(num >= 1 && num <= highlightCs.length)
    )
      num = 1;

    if (!cell) {
      if (currentTool === "Regions") {
        if (digits.includes(num))
          selection.forEach((a) => (a.region = num - 1));
      } else {
        if (!testPaused()) {
          for (var a = 0; a < selection.length; a++)
            selection[a].enter(num, false, a === selection.length - 1);

          if (testSolved()) {
            puzzleTimer.pause();
            finished = true;
          }
        }
      }

      generateCandidates();
    } else {
      cell.enter(num, true);

      var cloned = false;

      for (var a = 0; a < constraints[cID("Palindrome")].length; a++) {
        const palindrome = constraints[cID("Palindrome")][a];
        for (var b = 0; b < palindrome.lines.length; b++) {
          if (palindrome.lines[b].includes(cell)) {
            palindrome.lines[b][
              palindrome.lines[b].length - palindrome.lines[b].indexOf(cell) - 1
            ].enter(num, true);
            cloned = true;
          }
        }
      }

      for (var a = 0; a < constraints[cID("Clone")].length; a++) {
        const clone = constraints[cID("Clone")][a];
        if (clone.cells.includes(cell)) {
          clone.cloneCells[clone.cells.indexOf(cell)].enter(num, true);
          cloned = true;
        } else if (clone.cloneCells.includes(cell)) {
          clone.cells[clone.cloneCells.indexOf(cell)].enter(num, true);
          cloned = true;
        }
      }

      if (cloned && [undefined, true].includes(logProgress))
        log(";  Linked cells also filled", { newLine: false });
    }
  }
};

createGrid = function (newSize, clearHistory, refreshCandidates) {
  if (sizes[String(newSize)]) {
    clearGrid(true, false, refreshCandidates);

    size = tempSize = newSize;
    digits = [];
    for (var a = 1; a <= size; a++) digits.push(a);

    regionW = sizes[String(newSize)].w;
    regionH = sizes[String(newSize)].h;

    gridSL = canvas.height - gridTopMargin - gridBottomMargin;
    gridX = canvas.width / 2 - gridSL / 2;
    gridY = gridTopMargin;

    cellSL = gridSL / size;

    resetCells();
    createSidebars();

    generateSums();
    if (refreshCandidates) generateCandidates();

    if (clearHistory) {
      currentTool = lastTool = selectableConstraints[0];
      clearChangeHistory();
    }
  } else return "Invalid size";
};

clearGrid = function (hardReset, clearGivenPencils, refreshCandidates) {
  if (!hardReset) {
    for (var i = 0; i < size; i++) {
      for (var j = 0; j < size; j++) {
        if (
          !grid[i][j].given &&
          ([undefined, true].includes(clearGivenPencils) ||
            grid[i][j].candidates.length !== 1)
        )
          grid[i][j].value = 0;

        grid[i][j].cornerPencilMarks = [];
        if ([undefined, true].includes(clearGivenPencils)) {
          grid[i][j].centerPencilMarks = [];
          grid[i][j].highlight = 0;
        }
      }
    }
  } else {
    resetCells();
    createConstraints();
    createCosmetics();
  }

  selection = [];
  if ([undefined, true].includes(refreshCandidates)) generateCandidates();
};

resetCells = function () {
  grid = [];
  for (var i = 0; i < size; i++) {
    grid[i] = [];
    for (var j = 0; j < size; j++) grid[i][j] = new cell(i, j);
  }

  outsideGrid = [];
  for (var a = 0; a < 4; a++) {
    for (
      var b = a < 2 ? 0 : size - 1;
      a < 2 ? b <= size : b >= -1;
      b += a < 2 ? 1 : -1
    ) {
      i = a === 0 ? -1 : a === 2 ? size : b;
      j = a === 3 ? -1 : a === 1 ? size : b;
      outsideGrid.push(new cell(i, j, true));
    }
  }
};

createConstraints = function () {
  for (var a = 0; a < boolConstraints.length; a++)
    constraints[cID(boolConstraints[a])] = false;

  for (var a = 0; a < perCellConstraints.length; a++)
    constraints[cID(perCellConstraints[a])] = [];
  for (var a = 0; a < multicellConstraints.length; a++)
    constraints[cID(multicellConstraints[a])] = [];
  for (var a = 0; a < outsideConstraints.length; a++)
    constraints[cID(outsideConstraints[a])] = [];
};

createCosmetics = function () {
  for (var a = 0; a < toolCosmetics.length; a++) {
    if (cosmetics[cID(toolCosmetics[a])])
      cosmetics[cID(toolCosmetics[a])].length = 0;
    else cosmetics[cID(toolCosmetics[a])] = [];
  }
};

setUpCosmetics = function () {
  for (var a = 0; a < toolCosmetics.length; a++) {
    cosmetics[cID(toolCosmetics[a])] = [];
    cosmetics[cID(toolCosmetics[a])].baseC = "#FFFFFF";
    cosmetics[cID(toolCosmetics[a])].outlineC = "#000000";
    cosmetics[cID(toolCosmetics[a])].fontC = "#000000";
    cosmetics[cID(toolCosmetics[a])].size = 0.5;
    cosmetics[cID(toolCosmetics[a])].width = 0.5;
    cosmetics[cID(toolCosmetics[a])].height = 0.5;
    cosmetics[cID(toolCosmetics[a])].angle = 0;
  }
};

setCameraX = function (x) {
  cameraX = x;

  if (cameraX > 0) {
    consoleOutput.style.display = "block";
    document.getElementById("rules").style.display = "none";
  } else {
    consoleOutput.style.display = "none";
    showRules();
  }
};

initialize = (function () {
  updateImages();

  window.onload = function () {
    (function (a) {
      if (
        /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(
          a
        ) ||
        /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(
          a.substr(0, 4)
        )
      )
        mobile = true;
    })(navigator.userAgent || navigator.vendor || window.opera);

    categorizeTools();
    createGrid(size, true, true);

    for (var a = 0; a < boolSettings.length; a++)
      boolSettings[boolSettings[a]] = defaultSettings[a];
    loadSettings();

    createConstraints();
    createCosmetics();
    setUpCosmetics();

    if (location.search.substring(0, urlString.length) === urlString) {
      loaded = true;
      window.location.href =
        "https://tinyurl.com/" +
        location.search.substring(urlString.length, location.search.length);
    } else if (
      location.search.substring(0, importString.length) === importString
    ) {
      mode = "Solving";
      importPuzzle(
        location.search.substring(importString.length, location.search.length),
        true
      );
      showRules();
      puzzleTimer.restart(true);
    }

    if (!loaded) {
      cPicker.on("color:change", function () {
        document.activeElement.value = cPicker.color.hexString.toUpperCase();
        if (["baseC", "outlineC", "fontC"].includes(document.activeElement.id))
          updateCosmeticCs(document.activeElement.id);
      });

      document
        .getElementById("baseC")
        .addEventListener("input", (event) => updateCosmeticCs("baseC"));
      document
        .getElementById("outlineC")
        .addEventListener("input", (event) => updateCosmeticCs("outlineC"));
      document
        .getElementById("fontC")
        .addEventListener("input", (event) => updateCosmeticCs("fontC"));

      createSidebars();
      createOtherButtons();

      updateDarkMode();
      requestAnimationFrame(drawScreen);

      window.addEventListener("beforeunload", function (event) {
        const confirmationMessage =
          "Are you sure you want to close this tab? Your work will not be saved.";

        (event || window.event).returnValue = confirmationMessage;
        return confirmationMessage;
      });
    }
  };
})();
