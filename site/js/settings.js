const boolSettings = [
  "Dark Mode",
  "Show Tooltips",
  "Highlight Conflicts",
  "Highlight Cells Seen by Selection",
  "Display Candidates During Logic",
  "Treat Pencil Marks as Given",
  "Attempt Logic Before Brute Force",
  "Save Settings in Browser",
];
const defaultSettings = [false, true, true, false, true, false, true, false];
var bruteForceTimeLimit = 15; // Seconds
var solutionCountLimit = 100; // Solutions
var minStepDelay = 0.001; // Seconds
var generationAttempts = 50;

var saveDarkMode = null;

saveSettings = function () {
  if (boolSettings["Save Settings in Browser"]) {
    const savedSettings = {};

    boolSettings.forEach((a) => (savedSettings[a] = boolSettings[a]));

    savedSettings["bruteForceTimeLimit"] = bruteForceTimeLimit;
    savedSettings["solutionCountLimit"] = solutionCountLimit;
    savedSettings["minStepDelay"] = minStepDelay;
    savedSettings["generationAttempts"] = generationAttempts;

    localStorage.puzzleSetterSettings = JSON.stringify(savedSettings);
  }
};

loadSettings = function () {
  if (localStorage.puzzleSetterSettings) {
    const savedSettings = JSON.parse(localStorage["puzzleSetterSettings"]);

    boolSettings.forEach((a) => (boolSettings[a] = savedSettings[a]));

    document.getElementById("bruteForceTimeLimit").value =
      savedSettings["bruteForceTimeLimit"];
    document.getElementById("solutionCountLimit").value =
      savedSettings["solutionCountLimit"];
    document.getElementById("minStepDelay").value =
      savedSettings["minStepDelay"] * 1000;
    bruteForceTimeLimit = savedSettings["bruteForceTimeLimit"];
    solutionCountLimit = savedSettings["solutionCountLimit"];
    minStepDelay = savedSettings["minStepDelay"];
    generationAttempts = savedSettings["generationAttempts"];
  }
};
