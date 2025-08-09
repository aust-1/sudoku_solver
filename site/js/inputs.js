var mouseX = null;
var mouseY = null;
var holding = false;
var shifting = false;
var controlling = false;
var alting = false;
var disableInputs = false;

onInputStart = function (event) {
  updateHeldKeys(event);
};

onInputEnd = function () {
  if (!disableInputs) {
    resetKnownPuzzleInformation(true);

    if (!changeCancelled) {
      change = { state: exportPuzzle(true) };
      if (change.state !== changes[changeIndex].state || changeUndo) {
        change.solving = mode === "Solving";

        forgetFutureChanges();
        changes.push(change);
        changeIndex++;

        if (changeUndo) {
          changeUndo = false;
          undo(true);
        }
      }
    } else changeCancelled = false;
  }
};

updateCursorPosition = function (mouse) {
  mouseX =
    ((mouse.clientX - canvas.getBoundingClientRect().left) /
      canvas.getBoundingClientRect().width) *
      canvas.width +
    cameraX;
  mouseY =
    ((mouse.clientY - canvas.getBoundingClientRect().top) /
      canvas.getBoundingClientRect().height) *
    canvas.height;
};

document.onmousemove = function (mouse) {
  updateCursorPosition(mouse);

  if (!testPaused() && !disableInputs) {
    if (holding) {
      if (mode === "Solving" || selectableConstraints.includes(currentTool)) {
        for (var i = 0; i < size; i++) {
          for (var j = 0; j < size; j++) {
            if (grid[i][j].hovering()) grid[i][j].select();
          }
        }
      }

      if (mode === "Setting") useDraggableTools();
    }

    if (sidebars.length) {
      var hoveredButton =
        sidebars[sidebars.findIndex((a) => a.title === "Constraints")].buttons[
          sidebars[
            sidebars.findIndex((a) => a.title === "Constraints")
          ].buttons.findIndex((a) => a.id === "ConstraintTools")
        ];
      if (
        popup === "Constraint Tools" &&
        (mouseX < hoveredButton.x - hoveredButton.w / 2 - buttonMargin ||
          mouseX > hoveredButton.x + hoveredButton.w / 2 + buttonMargin ||
          mouseY < hoveredButton.y - buttonMargin ||
          mouseY > hoveredButton.y + buttonSH + buttonMargin) &&
        (mouseX < gridX - sidebarDist ||
          mouseX >
            gridX - sidebarDist + sidebarW + (buttonGap + buttonSH) * 2 ||
          mouseY <
            gridY +
              gridSL -
              (buttonSH * toolConstraints.length +
                buttonGap * (toolConstraints.length - 1) +
                buttonMargin * 2) ||
          mouseY > gridY + gridSL)
      )
        closePopups();
      var hoveredButton =
        sidebars[sidebars.findIndex((a) => a.title === "Constraints")].buttons[
          sidebars[
            sidebars.findIndex((a) => a.title === "Constraints")
          ].buttons.findIndex((a) => a.id === "CosmeticTools")
        ];
      if (
        popup === "Cosmetic Tools" &&
        (mouseX < hoveredButton.x - hoveredButton.w / 2 - buttonMargin ||
          mouseX > hoveredButton.x + hoveredButton.w / 2 + buttonMargin ||
          mouseY < hoveredButton.y - buttonMargin ||
          mouseY > hoveredButton.y + buttonSH + buttonMargin) &&
        (mouseX < gridX - sidebarDist ||
          mouseX > gridX - sidebarDist + sidebarW ||
          mouseY <
            gridY +
              gridSL -
              (buttonSH * toolCosmetics.length +
                buttonGap * (toolCosmetics.length - 1) +
                buttonMargin * 2) ||
          mouseY > gridY + gridSL) &&
        (!toolCosmetics.includes(currentTool) ||
          mouseX < gridX - sidebarDist + sidebarW ||
          mouseX > gridX - sidebarDist + sidebarW * 2 ||
          mouseY < cosmeticEditMenuY ||
          mouseY > cosmeticEditMenuY + cosmeticEditMenuH) &&
        (document.getElementById("colorPicker").style.display === "none" ||
          mouseX <
            gridX -
              sidebarDist +
              sidebarW * 2 -
              cosmeticEditMenuCloseForgiveness ||
          mouseX >
            gridX -
              sidebarDist +
              sidebarW * 2 +
              175 +
              cosmeticEditMenuCloseForgiveness ||
          mouseY <
            cosmeticEditMenuY +
              cosmeticEditMenuH -
              cPickerH -
              cosmeticEditMenuCloseForgiveness ||
          mouseY >
            cosmeticEditMenuY +
              cosmeticEditMenuH +
              cosmeticEditMenuCloseForgiveness)
      )
        closePopups();
    }

    for (var a = 0; a < sidebars.length; a++) {
      for (var b = 0; b < sidebars[a].buttons.length; b++) {
        if (sidebars[a].buttons[b].hoverable && sidebars[a].buttons[b].click())
          return onInputEnd();
      }
    }
    for (var a = 0; a < buttons.length; a++) {
      if (buttons[a].hoverable && buttons[a].click()) return onInputEnd();
    }
  }
};

document.onmousedown = function (mouse, override) {
  if (!mobile || override) {
    onInputStart(mouse);

    if (!disableInputs) {
      if (shifting) dragShift = true;

      for (var a = 0; a < sidebars.length; a++) {
        for (var b = 0; b < sidebars[a].buttons.length; b++) {
          if (sidebars[a].buttons[b].click()) return onInputEnd();
        }
      }
      for (var a = 0; a < buttons.length; a++) {
        if (buttons[a].click()) return onInputEnd();
      }

      if (popup) {
        if (
          (popup === "Constraint Tools" &&
            (mouseX < gridX - sidebarDist ||
              mouseX >
                gridX - sidebarDist + sidebarW + (buttonGap + buttonSH) * 2 ||
              mouseY <
                gridY +
                  gridSL -
                  (buttonSH * toolConstraints.length +
                    buttonGap * (toolConstraints.length - 1) +
                    buttonMargin * 2) ||
              mouseY > gridY + gridSL)) ||
          (popups[cID(popup)] &&
            (mouseX < canvas.width / 2 - popups[cID(popup)].w / 2 ||
              mouseX > canvas.width / 2 + popups[cID(popup)].w / 2 ||
              mouseY < canvas.height / 2 - popups[cID(popup)].h / 2 ||
              mouseY > canvas.height / 2 + popups[cID(popup)].h / 2))
        )
          closePopups();
        else return onInputEnd();
      }

      confirmSolve = false;
      confirmClear = false;
      confirmClearTimer = false;

      if (!testPaused()) {
        if (mouseInGrid() || !draggableTools.includes(currentTool))
          holding = true;

        if (
          !shifting &&
          !controlling &&
          !(
            mobile &&
            sidebars.some(
              (a) =>
                mouseX > a.x - sidebarW / 2 &&
                mouseX < a.x + sidebarW / 2 &&
                mouseY > gridY &&
                mouseY < gridY + gridSL
            )
          )
        )
          selection = [];
        getCells().forEach((a) => a.click());
        outsideGrid.forEach((a) => a.click());
      }
    }

    onInputEnd();
  }
};

document.onmouseup = function (mouse, override) {
  if (!mobile || override) {
    onInputStart(mouse);

    holding = false;
    dragAnchor = null;
    dragShift = false;

    if (!disableInputs) doneDraggingTool();

    onInputEnd();
  }
};

document.ontouchmove = function (mouse) {
  document.onmousemove(mouse.touches[0]);
};
document.ontouchstart = function (mouse) {
  updateCursorPosition(mouse.touches[0]);
  document.onmousedown(mouse, true);
};
document.ontouchend = function (mouse) {
  document.onmouseup(mouse, true);
  setTimeout(function () {
    mouseX = 0;
    mouseY = 0;
  }, 1);
};

document.oncontextmenu = function (event) {
  event.preventDefault();
};

document.onkeydown = function (event) {
  if (
    !event.repeat ||
    (controlling && ["Z", "Y"].includes(event.key.toUpperCase())) ||
    event.key === "Backspace"
  ) {
    onInputStart(event);

    if (!disableInputs) {
      if (mode === "Solving" && event.key === " ") puzzleTimer.toggle();

      if (event.key === "Escape") {
        setCameraX(0);
        closePopups();
      }

      if (!testPaused() && !popup) {
        if (controlling || !typeCosmetic(event.key)) {
          var eventNum = parseInt(event.keyCode) - 96;
          if (eventNum < 0) eventNum = parseInt(event.keyCode) - 48;

          if ("1234567890".split("").includes(String(eventNum))) {
            event.preventDefault();
            if (
              (alting || eventNum === 0) &&
              (selectableTools.includes(currentTool) ||
                currentTool === "Quadruple") &&
              (tempEnterMode === "Highlight"
                ? eventNum + 10 <= highlightCs.length
                : eventNum + 10 <= size)
            )
              eventNum += 10;

            if (!typeConstraint(eventNum)) enter(eventNum);
          }

          if ("XV".includes(event.key.toUpperCase())) {
            if (currentTool === "XV" && constraints[cID("XV")].length)
              constraints[cID("XV")][constraints[cID("XV")].length - 1].value =
                event.key.toUpperCase();
          }

          if (event.key === "Backspace" || event.key === "Delete") {
            event.preventDefault();

            if (!typeConstraint(event.key) && !typeCosmetic(event.key)) {
              if (
                mode === "Solving" ||
                selectableConstraints.includes(currentTool)
              )
                enter(0);
            }
          }

          if (selection.length) {
            if (
              ["ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft"].includes(
                event.key
              )
            ) {
              event.preventDefault();

              if (event.key === "ArrowUp")
                newCell =
                  grid[(selection[selection.length - 1].i - 1 + size) % size][
                    selection[selection.length - 1].j
                  ];
              if (event.key === "ArrowRight")
                newCell =
                  grid[selection[selection.length - 1].i][
                    (selection[selection.length - 1].j + 1 + size) % size
                  ];
              if (event.key === "ArrowDown")
                newCell =
                  grid[(selection[selection.length - 1].i + 1 + size) % size][
                    selection[selection.length - 1].j
                  ];
              if (event.key === "ArrowLeft")
                newCell =
                  grid[selection[selection.length - 1].i][
                    (selection[selection.length - 1].j - 1 + size) % size
                  ];
              if (shifting || controlling) {
                newCell.select();
                selection.push(
                  selection.splice(selection.indexOf(newCell), 1)[0]
                );
              } else selection = [newCell];
            }
          } else {
            if (
              ["ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft"].includes(
                event.key
              )
            )
              selection.push(grid[0][0]);
          }

          if (
            event.key.toUpperCase() === "A" &&
            controlling &&
            selectableConstraints.includes(currentTool)
          ) {
            if (document.activeElement === document.body) {
              event.preventDefault();
              selection = getCells();
            }
          }

          if (
            event.key.toUpperCase() === "G" &&
            controlling &&
            mode === "Setting"
          ) {
            if (event.ctrlKey) event.preventDefault();
            if (currentTool === "Given Digit") setCurrentTool(lastTool);
            else setCurrentTool("Given Digit");
          }

          if (event.key.toUpperCase() === "Y") {
            if (controlling) redo();
          }
          if (event.key.toUpperCase() === "Z") {
            if (controlling) {
              console.log("test");
              if (!testPaused()) {
                if (shifting) redo();
                else undo();
              }
            } else setEnterMode("Normal");
          }
          if (event.key.toUpperCase() === "X" && currentTool !== "XV")
            setEnterMode("Corner");
          if (event.key.toUpperCase() === "C") setEnterMode("Center");
          if (event.key.toUpperCase() === "V" && currentTool !== "XV")
            setEnterMode("Highlight");

          if (currentTool === "Given Digit") {
            if (event.key === "Shift") tempEnterMode = "Corner";
            if (event.key === "Control") tempEnterMode = "Center";
            createSidebars();
          }
        }
      }

      if (event.key === "Enter") {
        if (
          popup === "Edit Info" &&
          document.activeElement !== document.getElementById("ruleset")
        )
          setPuzzleInfo();
      }
    }

    onInputEnd();
  } else if (!testPaused() && !popup) event.preventDefault();
};

document.onkeyup = function (event) {
  onInputStart(event);

  if (currentTool === "Given Digit") {
    if (["Shift", "Control"].includes(event.key)) {
      tempEnterMode = enterMode;
      createSidebars();
    }
  }

  onInputEnd();
};

document.getElementById("bruteForceTimeLimit").oninput = function () {
  bruteForceTimeLimit = parseInt(
    document.getElementById("bruteForceTimeLimit").value
  );
  saveSettings();
};

document.getElementById("solutionCountLimit").oninput = function () {
  solutionCountLimit = parseInt(
    document.getElementById("solutionCountLimit").value
  );
  saveSettings();
};

document.getElementById("minStepDelay").oninput = function () {
  minStepDelay = parseInt(document.getElementById("minStepDelay").value) / 1000;
  saveSettings();
};
