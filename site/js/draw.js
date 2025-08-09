updateDarkMode = function () {
  if (boolSettings["Dark Mode"]) {
    document.body.style.backgroundColor = "#505050";
    document
      .querySelectorAll(".slider")
      .forEach((a) => (a.style.background = "#303030"));
    document
      .querySelectorAll(".switch")
      .forEach((a) => (a.style.background = "#303030"));
    document
      .querySelectorAll(".color")
      .forEach((a) => (a.style.background = "#303030"));
    document
      .querySelectorAll(".text")
      .forEach((a) => (a.style.background = "#303030"));
    document
      .querySelectorAll(".textarea")
      .forEach((a) => (a.style.background = "#303030"));
    document
      .querySelectorAll(".color")
      .forEach((a) => (a.style.color = "#FFFFFF"));
    document
      .querySelectorAll(".text")
      .forEach((a) => (a.style.color = "#FFFFFF"));
    document
      .querySelectorAll(".textarea")
      .forEach((a) => (a.style.color = "#FFFFFF"));
    highlightCs[0] = "#404040";
  } else {
    document.body.style.backgroundColor = "#FFFFFF";
    document
      .querySelectorAll(".slider")
      .forEach((a) => (a.style.background = "#D0D0D0"));
    document
      .querySelectorAll(".switch")
      .forEach((a) => (a.style.background = "#D0D0D0"));
    document
      .querySelectorAll(".color")
      .forEach((a) => (a.style.background = "#F0F0F0"));
    document
      .querySelectorAll(".text")
      .forEach((a) => (a.style.background = "#F0F0F0"));
    document
      .querySelectorAll(".textarea")
      .forEach((a) => (a.style.background = "#F0F0F0"));
    document
      .querySelectorAll(".color")
      .forEach((a) => (a.style.color = "#000000"));
    document
      .querySelectorAll(".text")
      .forEach((a) => (a.style.color = "#000000"));
    document
      .querySelectorAll(".textarea")
      .forEach((a) => (a.style.color = "#000000"));
    highlightCs[0] = "#FFFFFF";
  }

  updateImages();
  if (toolCosmetics.includes(currentTool)) {
    updateCosmeticCs("baseC", true);
    updateCosmeticCs("outlineC", true);
    updateCosmeticCs("fontC", true);
  }
};

drawScreen = function (step, forced) {
  ctx.fillStyle = boolSettings["Dark Mode"] ? "#505050" : "#FFFFFF";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.save();
  ctx.translate(-cameraX, 0);

  ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
  const title = getPuzzleTitle();
  ctx.font = (author.length ? titleSSize : titleLSize) + "px Arial";
  ctx.fillText(title, canvas.width / 2, author.length ? 55 : 70);
  if (author.length) {
    ctx.font = "16px Arial";
    ctx.fillText("by " + author, canvas.width / 2, 80);
  }

  if (!testPaused()) drawGrid();
  else {
    ctx.fillStyle = highlightCs[0];
    ctx.fillRect(gridX, gridY, gridSL, gridSL);
    ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
    ctx.font = "150px Arial";
    ctx.fillText("Paused", canvas.width / 2, canvas.height * 0.6);

    ctx.lineWidth = lineWW;
    ctx.strokeStyle = "#000000";
    ctx.strokeRect(gridX, gridY, gridSL, gridSL);
  }

  drawPopups(false);

  for (var a = 0; a < sidebars.length; a++) sidebars[a].show();
  if (boolSettings["Show Tooltips"]) {
    for (var a = 0; a < sidebars.length; a++) sidebars[a].showTooltip();
  }

  drawPopups(true);

  if (mode === "Solving") {
    ctx.fillStyle = finished
      ? "#20FF20"
      : boolSettings["Dark Mode"]
      ? "#F0F0F0"
      : "#202020";
    ctx.font = "60px Arial";
    ctx.fillText(
      puzzleTimer.shown ? puzzleTimer.getTime() : "??:??",
      gridX - (sidebarDist + sidebarW / 2),
      gridY + sidebarTitleHeight + 190
    );
  }

  for (var a = 0; a < buttons.length; a++) buttons[a].show();

  ctx.restore();

  ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
  ctx.font = "12px Arial";
  ctx.fillText(
    "Eliott A. Roussille. MIT License.",
    canvas.width / 2,
    gridY + gridSL + 25
  );

  if (!forced) requestAnimationFrame(drawScreen);
};

drawGrid = function () {
  ctx.fillStyle = boolSettings["Dark Mode"] ? "#505050" : "#FFFFFF";
  ctx.fillRect(gridX, gridY, gridSL, gridSL);

  if (outsideConstraintsVisible()) {
    ctx.save();
    ctx.translate(
      gridX - ((gridX - cellSL) * gridSL) / (gridSL + 2 * cellSL),
      gridY - ((gridY - cellSL) * gridSL) / (gridSL + 2 * cellSL)
    );
    ctx.scale(gridSL / (gridSL + 2 * cellSL), gridSL / (gridSL + 2 * cellSL));
  }

  for (var i = 0; i < size; i++) {
    for (var j = 0; j < size; j++) grid[i][j].showBottom();
  }

  drawConstraints("Bottom");

  cellsSeenBySelection = [];
  if (boolSettings["Highlight Cells Seen by Selection"])
    cellsSeenBySelection = getCellsSeenByCells(selection);
  getCells().forEach((a) => a.showSelection());
  getCells().forEach((a) => a.showOutline());

  drawCosmetics();

  getCells().forEach((a) => a.showTop());

  drawConstraints("Top");

  if (outsideConstraintsVisible()) ctx.restore();
};

drawConstraints = function (layer) {
  if (layer === "Bottom") {
    for (var a = 0; a < constraints[cID("Extra Region")].length; a++)
      constraints[cID("Extra Region")][a].show();
    for (var a = 0; a < constraints[cID("Clone")].length; a++)
      constraints[cID("Clone")][a].show();
    for (var a = 0; a < constraints[cID("Thermometer")].length; a++)
      constraints[cID("Thermometer")][a].show();
    /*for(var a = 0; a < constraints[cID('Slow Thermometer')].length; a++)
			constraints[cID('Slow Thermometer')][a].show();*/
    for (var a = 0; a < constraints[cID("Minimum")].length; a++)
      constraints[cID("Minimum")][a].show();
    for (var a = 0; a < constraints[cID("Maximum")].length; a++)
      constraints[cID("Maximum")][a].show();
    for (var a = 0; a < constraints[cID("Palindrome")].length; a++)
      constraints[cID("Palindrome")][a].show();
    for (var a = 0; a < constraints[cID("Between Line")].length; a++)
      constraints[cID("Between Line")][a].show();
    for (var a = 0; a < constraints[cID("Arrow")].length; a++)
      constraints[cID("Arrow")][a].show();

    if (constraints[cID("Diagonal +")]) {
      ctx.lineWidth = lineWT;
      ctx.strokeStyle = "#000000";
      ctx.beginPath();
      ctx.moveTo(gridX + gridSL, gridY);
      ctx.lineTo(gridX, gridY + gridSL);
      ctx.stroke();
    }

    if (constraints[cID("Diagonal -")]) {
      ctx.lineWidth = lineWT;
      ctx.strokeStyle = "#000000";
      ctx.beginPath();
      ctx.moveTo(gridX, gridY);
      ctx.lineTo(gridX + gridSL, gridY + gridSL);
      ctx.stroke();
    }

    for (var a = 0; a < constraints[cID("Killer Cage")].length; a++)
      constraints[cID("Killer Cage")][a].show();

    for (var a = 0; a < constraints[cID("Odd")].length; a++)
      constraints[cID("Odd")][a].show();
    for (var a = 0; a < constraints[cID("Even")].length; a++)
      constraints[cID("Even")][a].show();
  }

  if (layer === "Top") {
    for (var a = 0; a < constraints[cID("XV")].length; a++)
      constraints[cID("XV")][a].show();
    for (var a = 0; a < constraints[cID("Quadruple")].length; a++)
      constraints[cID("Quadruple")][a].show();
    for (var a = 0; a < constraints[cID("Difference")].length; a++)
      constraints[cID("Difference")][a].show();
    for (var a = 0; a < constraints[cID("Ratio")].length; a++)
      constraints[cID("Ratio")][a].show();

    for (var a = 0; a < constraints[cID("Little Killer Sum")].length; a++)
      constraints[cID("Little Killer Sum")][a].show();
    for (var a = 0; a < constraints[cID("Sandwich Sum")].length; a++)
      constraints[cID("Sandwich Sum")][a].show();
  }
};

drawCosmetics = function () {
  for (var a = 0; a < cosmetics[cID("Rectangle")].length; a++)
    cosmetics[cID("Rectangle")][a].show();
  for (var a = 0; a < cosmetics[cID("Circle")].length; a++)
    cosmetics[cID("Circle")][a].show();

  for (var a = 0; a < cosmetics[cID("Cage")].length; a++)
    cosmetics[cID("Cage")][a].show();

  for (var a = 0; a < cosmetics[cID("Line")].length; a++)
    cosmetics[cID("Line")][a].show();

  for (var a = 0; a < cosmetics[cID("Text")].length; a++)
    cosmetics[cID("Text")][a].show();
};

drawPopups = function (overlapSidebars) {
  var box = null;
  if (overlapSidebars && popup && popups[cID(popup)]) {
    box = popups[cID(popup)];

    ctx.lineWidth = lineWW;
    ctx.fillStyle = boolSettings["Dark Mode"] ? "#505050" : "#F0F0F0";
    ctx.strokeStyle = "#000000";
    ctx.fillRect(
      canvas.width / 2 - box.w / 2,
      canvas.height / 2 - box.h / 2,
      box.w,
      box.h
    );
    ctx.strokeRect(
      canvas.width / 2 - box.w / 2,
      canvas.height / 2 - box.h / 2,
      box.w,
      box.h
    );
  }

  if (overlapSidebars) {
    if (popup === "Info") {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#E0E0E0";
      ctx.strokeStyle = "#000000";
      ctx.fillRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        90
      );
      ctx.strokeRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        90
      );

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = "50px Arial";
      ctx.fillText(
        "Welcome to f-puzzles.com!",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 64
      );

      ctx.font = "38px Arial";
      ctx.fillText(
        "Here, you can create and solve",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 140
      );
      ctx.fillText(
        "all sorts of Sudoku variants!",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 180
      );

      ctx.font = "bold 28px Arial";
      ctx.fillText(
        "Shortcuts:",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 230
      );
      ctx.font = "20px Arial";
      ctx.fillText(
        'z - Select "Normal" enter mode',
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 260
      );
      ctx.fillText(
        'x - Select "Center" enter mode',
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 280
      );
      ctx.fillText(
        'c - Select "Corner" enter mode',
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 300
      );
      ctx.fillText(
        'v - Select "Highlight" enter mode',
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 320
      );
      ctx.fillText(
        "ctrl+z - Undo",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 340
      );
      ctx.fillText(
        "ctrl+y - Redo",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 360
      );
      ctx.fillText(
        "ctrl+a - Select all cells",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 380
      );
      ctx.fillText(
        'ctrl+g - Switch to/from "Given Digit"',
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 400
      );
      ctx.fillText(
        "space - Pause/unpause when solving",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 420
      );
    }

    if (popup === "Settings") {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#E0E0E0";
      ctx.strokeStyle = "#000000";
      ctx.fillRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        90
      );
      ctx.strokeRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        90
      );

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = "60px Arial";
      ctx.fillText(
        "Settings",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 66
      );

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = "bold 20px Arial";
      ctx.fillText(
        "Brute Force Time Limit: " + bruteForceTimeLimit + "s",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 454
      );
      ctx.fillText(
        "Solution Count Limit: " + solutionCountLimit,
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 522
      );
      ctx.fillText(
        "Solution Path Step Delay: " + minStepDelay.toFixed(3) + "s",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 590
      );
    }

    if (popup === "New Grid") {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#E0E0E0";
      ctx.strokeStyle = "#000000";
      ctx.fillRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        87.5
      );
      ctx.strokeRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        87.5
      );

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = "55px Arial";
      ctx.fillText(
        "Select a grid size:",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 62.5
      );

      ctx.font = "60px Arial";
      ctx.fillText(
        tempSize + "x" + tempSize,
        canvas.width / 2,
        canvas.height / 2 + box.h * 0.123
      );
    }

    if (popup === "Export") {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#E0E0E0";
      ctx.strokeStyle = "#000000";
      ctx.fillRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        100
      );
      ctx.strokeRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        100
      );

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = "60px Arial";
      ctx.fillText(
        "Export Puzzle",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 70
      );

      ctx.font = "30px Arial";
      ctx.fillText(
        "Preview Mode",
        canvas.width / 2 - 175,
        canvas.height / 2 - box.h / 2 + 145
      );
      ctx.font = "25px Arial";
      ctx.fillText(
        "Image",
        canvas.width / 2 - 270,
        canvas.height / 2 - box.h / 2 + 185
      );
      ctx.fillText(
        "SS/Link",
        canvas.width / 2 - 77,
        canvas.height / 2 - box.h / 2 + 185
      );

      ctx.font = "30px Arial";
      ctx.fillText(
        "Preview",
        canvas.width / 2 + 230,
        canvas.height / 2 - box.h / 2 + 145
      );

      togglePreview(document.getElementById("previewType").checked);

      ctx.save();
      ctx.translate(
        canvas.width / 2 - gridX + 330,
        canvas.height / 2 - gridY - 20
      );
      ctx.scale(0.4, 0.4);
      drawGrid();
      ctx.restore();

      togglePreview(document.getElementById("previewType").checked);
    }

    if (popup === "Edit Info") {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#E0E0E0";
      ctx.strokeStyle = "#000000";
      ctx.fillRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        100
      );
      ctx.strokeRect(
        canvas.width / 2 - box.w / 2,
        canvas.height / 2 - box.h / 2,
        box.w,
        100
      );

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = "60px Arial";
      ctx.fillText(
        "Edit Puzzle Information",
        canvas.width / 2,
        canvas.height / 2 - box.h / 2 + 70
      );

      ctx.font = "30px Arial";
      ctx.fillText("by", canvas.width / 2, canvas.height / 2 - box.h / 2 + 215);
    }
  } else {
    if (popup === "Constraint Tools") {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#D0D0D0";
      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#202020" : "#808080";
      ctx.fillRect(
        gridX - sidebarDist,
        gridY + gridSL,
        sidebarW + (buttonGap + buttonSH) * 2,
        -(
          buttonSH * toolConstraints.length +
          buttonGap * (toolConstraints.length - 1) +
          buttonMargin * 2
        )
      );
      ctx.strokeRect(
        gridX - sidebarDist,
        gridY + gridSL,
        sidebarW + (buttonGap + buttonSH) * 2,
        -(
          buttonSH * toolConstraints.length +
          buttonGap * (toolConstraints.length - 1) +
          buttonMargin * 2
        )
      );
    }

    if (popup === "Cosmetic Tools") {
      if (
        [
          document.getElementById("baseC"),
          document.getElementById("outlineC"),
          document.getElementById("fontC"),
        ].includes(document.activeElement)
      ) {
        document.getElementById("colorPicker").style.display = "block";
        if (/^#[0-9A-F]{6}$/i.test(document.activeElement.value))
          cPicker.color.hexString = document.activeElement.value;
      } else document.getElementById("colorPicker").style.display = "none";

      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#D0D0D0";
      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#202020" : "#808080";
      ctx.fillRect(
        gridX - sidebarDist,
        gridY + gridSL,
        sidebarW,
        -(
          buttonSH * toolCosmetics.length +
          buttonGap * (toolCosmetics.length - 1) +
          buttonMargin * 2
        )
      );
      ctx.strokeRect(
        gridX - sidebarDist,
        gridY + gridSL,
        sidebarW,
        -(
          buttonSH * toolCosmetics.length +
          buttonGap * (toolCosmetics.length - 1) +
          buttonMargin * 2
        )
      );
      if (toolCosmetics.includes(currentTool)) {
        ctx.fillRect(
          gridX - sidebarDist + sidebarW,
          cosmeticEditMenuY,
          sidebarW,
          cosmeticEditMenuH
        );
        ctx.strokeRect(
          gridX - sidebarDist + sidebarW,
          cosmeticEditMenuY,
          sidebarW,
          cosmeticEditMenuH
        );
        if (document.getElementById("colorPicker").style.display === "block") {
          ctx.fillRect(
            gridX - sidebarDist + sidebarW * 2,
            cosmeticEditMenuY + cosmeticEditMenuH - cPickerH,
            175,
            cPickerH
          );
          ctx.strokeRect(
            gridX - sidebarDist + sidebarW * 2,
            cosmeticEditMenuY + cosmeticEditMenuH - cPickerH,
            175,
            cPickerH
          );
        }
      }

      const btns = sidebars[0].buttons;
      const btnsToMove = [
        "CosmeticPlaceMode",
        "CosmeticSizeL",
        "CosmeticSizeR",
        "CosmeticWL",
        "CosmeticWR",
        "CosmeticHL",
        "CosmeticHR",
        "CosmeticAngleL",
        "CosmeticAngleR",
      ];
      for (var a = 0; a < btnsToMove.length; a++)
        btns[btns.findIndex((b) => b.id === btnsToMove[a])].y = -1000;
      document.getElementById("baseC").style.display = "none";
      document.getElementById("outlineC").style.display = "none";
      document.getElementById("fontC").style.display = "none";

      if (toolCosmetics.includes(currentTool)) {
        const sampleObj = new window[cID(currentTool)]([]);
        var y = cosmeticEditMenuY + buttonMargin - buttonSH - buttonGap;
        cPicker.resize(canvas.clientWidth * 0.1);
        document.getElementById("colorPicker").style.top =
          100 *
            ((cosmeticEditMenuY + cosmeticEditMenuH - cPickerH) /
              canvas.height) +
          1 +
          "%";
        setTimeout(function () {
          cPicker.setOptions({
            margin: canvas.clientWidth * 0.001,
            borderWidth: canvas.clientWidth * 0.004,
          });
        }, 1);

        ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
        ctx.font = "bold 24px Arial";
        if (undraggableCosmetics.includes(currentTool)) {
          y += buttonSH + buttonGap;
          btns[btns.findIndex((a) => a.id === "CosmeticPlaceMode")].y = y;
          y += 15;
        }
        if (sampleObj.size !== undefined) {
          y += buttonSH + buttonGap;
          btns[btns.findIndex((a) => a.id === "CosmeticSizeL")].y = y;
          btns[btns.findIndex((a) => a.id === "CosmeticSizeR")].y = y;
          ctx.fillText(
            "Size: " + cosmetics[cID(currentTool)].size.toFixed(2),
            gridX - sidebarDist + sidebarW * 1.5,
            y + buttonSH * 0.8
          );
        }
        if (sampleObj.width !== undefined) {
          y += buttonSH + buttonGap;
          btns[btns.findIndex((a) => a.id === "CosmeticWL")].y = y;
          btns[btns.findIndex((a) => a.id === "CosmeticWR")].y = y;
          ctx.fillText(
            "Width: " + cosmetics[cID(currentTool)].width.toFixed(2),
            gridX - sidebarDist + sidebarW * 1.5,
            y + buttonSH * 0.8
          );
        }
        if (sampleObj.height !== undefined) {
          y += buttonSH + buttonGap;
          btns[btns.findIndex((a) => a.id === "CosmeticHL")].y = y;
          btns[btns.findIndex((a) => a.id === "CosmeticHR")].y = y;
          ctx.fillText(
            "Height: " + cosmetics[cID(currentTool)].height.toFixed(2),
            gridX - sidebarDist + sidebarW * 1.5,
            y + buttonSH * 0.8
          );
        }
        if (sampleObj.angle !== undefined) {
          y += buttonSH + buttonGap;
          btns[btns.findIndex((a) => a.id === "CosmeticAngleL")].y = y;
          btns[btns.findIndex((a) => a.id === "CosmeticAngleR")].y = y;
          ctx.fillText(
            "Angle: " + cosmetics[cID(currentTool)].angle + "°",
            gridX - sidebarDist + sidebarW * 1.5,
            y + buttonSH * 0.8
          );
        }

        ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
        ctx.font = "bold 16px Arial";
        if (sampleObj.baseC) {
          y += buttonSH + cosmeticEditMenuCBoxGap;
          ctx.fillText(
            "Base",
            gridX - sidebarDist + sidebarW * 1.5,
            y - buttonSH * 0.2
          );
          document.getElementById("baseC").style.top =
            100 * (y / canvas.height) - 0.3 + "%";
          document.getElementById("baseC").style.display = "block";
        }
        if (sampleObj.outlineC) {
          y += buttonSH + cosmeticEditMenuCBoxGap;
          ctx.fillText(
            "Outline",
            gridX - sidebarDist + sidebarW * 1.5,
            y - buttonSH * 0.2
          );
          document.getElementById("outlineC").style.top =
            100 * (y / canvas.height) - 0.3 + "%";
          document.getElementById("outlineC").style.display = "block";
        }
        if (sampleObj.fontC) {
          y += buttonSH + cosmeticEditMenuCBoxGap;
          ctx.fillText(
            "Text",
            gridX - sidebarDist + sidebarW * 1.5,
            y - buttonSH * 0.2
          );
          document.getElementById("fontC").style.top =
            100 * (y / canvas.height) - 0.3 + "%";
          document.getElementById("fontC").style.display = "block";
        }
      }
    }
  }
};
