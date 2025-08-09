undo = function (forget) {
  changeCancelled = true;
  holding = false;

  if (changeIndex > 0) {
    if (changes[changeIndex].solving || mode === "Setting") {
      changeIndex--;
      importPuzzle(changes[changeIndex].state, false);
      if (forget) forgetFutureChanges();
    }
  }

  untaintedFromLastStep = false;
};

redo = function () {
  changeCancelled = true;
  holding = false;

  if (changeIndex < changes.length - 1) {
    if (changes[changeIndex + 1].solving || mode === "Setting") {
      changeIndex++;
      importPuzzle(changes[changeIndex].state, false);
    }
  }

  untaintedFromLastStep = false;
};

forgetFutureChanges = function () {
  changes = changes.slice(0, changeIndex + 1);
};

clearChangeHistory = function () {
  changes = [];
  changeIndex = 0;

  changes.push({ state: exportPuzzle(true), solving: mode === "Solving" });
};
