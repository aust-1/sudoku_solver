button = function (x, y, w, h, modes, id, title, showBackground, hoverable) {
  this.x = x;
  this.y = y;
  this.w = w;
  this.h = h;

  this.modes = modes;
  this.hoverable = hoverable;

  this.id = id;
  this.title = title;

  this.showBackground = showBackground;

  this.correctMode = function () {
    return this.modes.includes(mode) || this.modes.includes(popup);
  };

  this.hovering = function () {
    if (
      disableInputs ||
      mouseX - cameraX < 0 ||
      mouseX - cameraX > canvas.width ||
      mouseY < 0 ||
      mouseY > canvas.height
    )
      return false;
    return (
      this.correctMode() &&
      mouseX >= this.x - this.w / 2 &&
      mouseX <= this.x + this.w / 2 &&
      mouseY >= this.y &&
      mouseY <= this.y + this.h
    );
  };

  this.click = function () {
    if (this.hovering()) {
      if (
        !this.modes.includes(popup) &&
        !["Settings", "New", "ConstraintTools"].includes(this.id)
      )
        closePopups();

      if (this.id === "Info") togglePopup("Info");

      if (this.id === "Settings") togglePopup("Settings");

      if (boolSettings.includes(this.id)) {
        boolSettings[this.id] = !boolSettings[this.id];

        saveSettings();
        if (!boolSettings["Save Settings in Browser"])
          localStorage.removeItem("puzzleSetterSettings");

        if (this.id === "Dark Mode") updateDarkMode();
      }

      if (this.id === "New") togglePopup("New Grid");

      if (this.id === "Size-") {
        if (sizes[String(tempSize - 1)]) tempSize--;
      }
      if (this.id === "Size+") {
        if (sizes[String(tempSize + 1)]) tempSize++;
      }

      if (this.id === "ConfirmNew") {
        createGrid(tempSize, false, true);
        closePopups();
      }

      if (this.id === "Export") togglePopup("Export");

      if (this.id === "DisableHC") disableHC = !disableHC;

      if (this.id === "Download") download();
      if (this.id === "Screenshot") download(true);
      if (this.id === "OpenLink") window.open(getLink());

      if (boolConstraints.includes(this.id)) {
        constraints[cID(this.id)] = !constraints[cID(this.id)];
        generateCandidates();
      }

      if (this.id === "ConstraintTools") togglePopup("Constraint Tools");

      if (
        selectableConstraints.includes(this.id) ||
        toolConstraints.includes(this.id)
      ) {
        setCurrentTool(this.id);
        closePopups();
      }
      if (
        negativableConstraints.includes(
          this.id.substring(0, this.id.length - 1)
        )
      )
        constraints[cID(this.id.substring(0, this.id.length - 1))].negative =
          !constraints[cID(this.id.substring(0, this.id.length - 1))].negative;

      if (this.id === "CosmeticTools") togglePopup("Cosmetic Tools");

      if (toolCosmetics.includes(this.id)) {
        setCurrentTool(this.id);
        const sampleObj = new window[cID(this.id)]([]);
        if (sampleObj.baseC)
          document.getElementById("baseC").value =
            cosmetics[cID(this.id)].baseC;
        if (sampleObj.outlineC)
          document.getElementById("outlineC").value =
            cosmetics[cID(this.id)].outlineC;
        if (sampleObj.fontC)
          document.getElementById("fontC").value =
            cosmetics[cID(this.id)].fontC;

        createCosmeticPopup(sampleObj);
        updateCosmeticCs("baseC", true);
        updateCosmeticCs("outlineC", true);
        updateCosmeticCs("fontC", true);
      }

      if (toolCosmetics.includes(currentTool)) {
        if (this.id === "CosmeticPlaceMode")
          cosmeticPlaceMode =
            cosmeticPlaceModes[
              (cosmeticPlaceModes.indexOf(cosmeticPlaceMode) + 1) %
                cosmeticPlaceModes.length
            ];
        if (
          this.id === "CosmeticSizeL" &&
          cosmetics[cID(currentTool)].size &&
          cosmetics[cID(currentTool)].size > cosmeticMinSize
        )
          cosmetics[cID(currentTool)].size = parseFloat(
            (cosmetics[cID(currentTool)].size - cosmeticSizeStep).toFixed(2)
          );
        if (
          this.id === "CosmeticSizeR" &&
          cosmetics[cID(currentTool)].size &&
          cosmetics[cID(currentTool)].size < cosmeticMaxSize
        )
          cosmetics[cID(currentTool)].size = parseFloat(
            (cosmetics[cID(currentTool)].size + cosmeticSizeStep).toFixed(2)
          );
        if (
          this.id === "CosmeticWL" &&
          cosmetics[cID(currentTool)].width &&
          cosmetics[cID(currentTool)].width > cosmeticMinSize
        )
          cosmetics[cID(currentTool)].width = parseFloat(
            (cosmetics[cID(currentTool)].width - cosmeticSizeStep).toFixed(2)
          );
        if (
          this.id === "CosmeticWR" &&
          cosmetics[cID(currentTool)].width &&
          cosmetics[cID(currentTool)].width < cosmeticMaxSize
        )
          cosmetics[cID(currentTool)].width = parseFloat(
            (cosmetics[cID(currentTool)].width + cosmeticSizeStep).toFixed(2)
          );
        if (
          this.id === "CosmeticHL" &&
          cosmetics[cID(currentTool)].height &&
          cosmetics[cID(currentTool)].height > cosmeticMinSize
        )
          cosmetics[cID(currentTool)].height = parseFloat(
            (cosmetics[cID(currentTool)].height - cosmeticSizeStep).toFixed(2)
          );
        if (
          this.id === "CosmeticHR" &&
          cosmetics[cID(currentTool)].height &&
          cosmetics[cID(currentTool)].height < cosmeticMaxSize
        )
          cosmetics[cID(currentTool)].height = parseFloat(
            (cosmetics[cID(currentTool)].height + cosmeticSizeStep).toFixed(2)
          );
        if (
          this.id === "CosmeticAngleL" &&
          cosmetics[cID(currentTool)].angle !== undefined
        )
          cosmetics[cID(currentTool)].angle -= cosmeticAngleStep;
        if (
          this.id === "CosmeticAngleR" &&
          cosmetics[cID(currentTool)].angle !== undefined
        )
          cosmetics[cID(currentTool)].angle += cosmeticAngleStep;
      }

      if (this.id === "EditInfo") togglePopup("Edit Info");
      if (this.id === "ConfirmInfo") setPuzzleInfo();

      if (this.id === "PauseTimer") puzzleTimer.toggle();
      if (this.id === "HideTimer") puzzleTimer.shown = !puzzleTimer.shown;
      if (this.id === "ClearTimer") {
        if (mode === "Setting" || confirmClearTimer) {
          puzzleTimer.restart(true);
          confirmClearTimer = false;
        } else confirmClearTimer = true;
      } else confirmClearTimer = false;

      if (this.id === "Mode") {
        if (mode === "Setting") {
          mode = "Solving";
          setCurrentTool("Given Digit");
          puzzleTimer.restart(true);
          finished = false;
          showRules();
        } else if (mode === "Solving") {
          mode = "Setting";
          document.getElementById("rules").style.display = "none";
        }

        createSidebars();
      }

      if (this.id === "Solve") {
        if (mode === "Setting" || confirmSolve) {
          disableInputs = true;
          solve();
          if (solveOutput === "Done") solve();
          confirmSolve = false;
        } else confirmSolve = true;
      } else confirmSolve = false;

      if (this.id === "Clear") {
        if (mode === "Setting" || confirmClear) {
          clearGrid(false, true);
          finished = false;
          puzzleTimer.start();
          confirmClear = false;
        } else confirmClear = true;
      } else confirmClear = false;

      if (this.id.substring(0, 5) === "Enter") setEnterMode(this.title);

      if (
        parseInt(this.id) == this.id ||
        (tempEnterMode === "Highlight" &&
          this.id >= 1 &&
          this.id <= highlightCs.length)
      ) {
        if (!typeConstraint(this.id) && !typeCosmetic(this.id))
          enter(parseInt(this.id));
      }
      if (this.id === "Delete") {
        if (!typeConstraint(this.id) && !typeCosmetic(this.id)) {
          if (mode === "Solving" || selectableConstraints.includes(currentTool))
            enter(0);
        }
      }

      if (this.id === "Undo") undo();
      if (this.id === "Redo") redo();

      if (
        ["SolvePath", "SolveStep", "CheckUnique", "CountSolutions"].includes(
          this.id
        )
      ) {
        if (mode === "Solving") {
          clearConsole();
          log("This feature is disabled in solving mode");
        } else {
          disableInputs = true;

          if (this.id === "SolvePath")
            solve({ logicOnly: true, animate: true });
          if (this.id === "SolveStep") {
            solve({ logicOnly: true, animate: false, oneStep: true });
            disableInputs = false;
          }
          if (this.id === "CheckUnique") countSolutions({}, true);
          if (this.id === "CountSolutions") countSolutions({});
        }
      }

      if (this.id === "Camera") {
        if (cameraX) setCameraX(0);
        else {
          if (this.x < canvas.width / 2) setCameraX(-cameraMoveAmount);
          if (this.x > canvas.width / 2) setCameraX(cameraMoveAmount);
        }
      }

      if (this.id === "X") closePopups();

      return true;
    } else return false;
  };

  this.show = function () {
    if (this.correctMode()) {
      const highlighted =
        this.hovering() ||
        currentTool === this.id ||
        tempEnterMode === this.title;

      this.showCheckBox();

      if (highlighted) {
        this.y -= this.h * 0.03;
        this.w *= 1.06;
        this.h *= 1.06;
      }

      if ([undefined, true].includes(this.showBackground)) {
        ctx.lineWidth = lineWW;
        if (highlighted)
          ctx.fillStyle = boolSettings["Dark Mode"] ? "#383838" : "#FFFFFF";
        else ctx.fillStyle = boolSettings["Dark Mode"] ? "#303030" : "#F0F0F0";
        ctx.strokeStyle = "#000000";
        ctx.fillRect(this.x - this.w / 2, this.y, this.w, this.h);
        ctx.strokeRect(this.x - this.w / 2, this.y, this.w, this.h);
      }

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      if (
        parseInt(this.id) == this.id ||
        (tempEnterMode === "Highlight" && this.id >= 1 && this.id <= 9)
      ) {
        if (tempEnterMode === "Normal") {
          ctx.font = this.h * 0.75 + "px Arial";
          ctx.fillText(this.id, this.x, this.y + this.h * 0.75);
        } else if (tempEnterMode === "Corner") {
          ctx.font = this.h * 0.35 + "px Arial";
          ctx.fillText(this.id, this.x - this.w * 0.35, this.y + this.h * 0.4);
        } else if (tempEnterMode === "Center") {
          ctx.font = this.h * 0.35 + "px Arial";
          ctx.fillText(this.id, this.x, this.y + this.h * 0.6);
        } else if (tempEnterMode === "Highlight") {
          ctx.lineWidth = lineWT;
          ctx.fillStyle = highlightCs[this.id - 1];
          ctx.strokeStyle = "#000000";
          ctx.fillRect(
            this.x - this.h * 0.3,
            this.y + this.h * 0.2,
            this.h * 0.6,
            this.h * 0.6
          );
          ctx.strokeRect(
            this.x - this.h * 0.3,
            this.y + this.h * 0.2,
            this.h * 0.6,
            this.h * 0.6
          );
        }
      } else if (this.id === "Mode") {
        ctx.font = "bold " + this.h * 0.75 + "px Arial";
        ctx.fillText("Mode: " + mode, this.x, this.y + this.h * 0.75);
      } else if (this.id === "Solve") {
        ctx.font = "bold " + this.h * 0.75 + "px Arial";
        ctx.fillText(
          confirmSolve ? "Confirm?" : "Solve",
          this.x,
          this.y + this.h * 0.75
        );
      } else if (this.id === "Clear") {
        ctx.font = "bold " + this.h * 0.75 + "px Arial";
        ctx.fillText(
          confirmClear ? "Confirm?" : "Clear",
          this.x,
          this.y + this.h * 0.75
        );
      } else if (this.id === "Camera") {
        ctx.font = "bold " + this.h * 0.888 + "px Arial";
        ctx.fillText(
          cameraX
            ? cameraX < 0
              ? "»"
              : "«"
            : this.x > canvas.width / 2
            ? "»"
            : "«",
          this.x,
          this.y + this.h * 0.75
        );
      } else if (this.id === "PauseTimer") {
        if (puzzleTimer.paused)
          ctx.drawImage(
            playIcon,
            this.x - this.h * 0.32,
            this.y + this.h * 0.18,
            this.h * 0.64,
            this.h * 0.64
          );
        else
          ctx.drawImage(
            pauseIcon,
            this.x - this.h * 0.32,
            this.y + this.h * 0.18,
            this.h * 0.64,
            this.h * 0.64
          );
      } else if (this.id === "HideTimer") {
        ctx.font = "bold " + this.h * 0.75 + "px Arial";
        ctx.fillText(
          puzzleTimer.shown ? "Hide" : "Show",
          this.x,
          this.y + this.h * 0.75
        );
      } else if (this.id === "ClearTimer") {
        if (confirmClearTimer) {
          ctx.font = "bold " + this.h * 0.5 + "px Arial";
          ctx.fillText("Confirm?", this.x, this.y + this.h * 0.68);
        } else {
          ctx.font = "bold " + this.h * 0.75 + "px Arial";
          ctx.fillText("Reset", this.x, this.y + this.h * 0.75);
        }
      } else if (this.id === "EditInfo") {
        ctx.drawImage(editIcon, this.x - this.w / 2, this.y, this.w, this.h);
      } else if (this.id === "CosmeticPlaceMode") {
        ctx.font = "bold " + this.h * 0.7 + "px Arial";
        ctx.fillText(
          "Place Mode: " + cosmeticPlaceMode,
          this.x,
          this.y + this.h * 0.75
        );
      } else {
        ctx.font = "bold " + this.h * 0.75 + "px Arial";
        ctx.fillText(this.title, this.x, this.y + this.h * 0.75);
      }

      if (highlighted) {
        this.w /= 1.06;
        this.h /= 1.06;
        this.y += this.h * 0.03;
      }
    }
  };

  this.showCheckBox = function () {
    if (
      boolSettings.includes(this.id) ||
      boolConstraints.includes(this.id) ||
      negativableConstraints.includes(
        this.id.substring(0, this.id.length - 1)
      ) ||
      this.id === "DisableHC"
    ) {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#606060" : "#A0A0A0";
      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#000000" : "#808080";
      ctx.fillRect(this.x + this.w / 2 + buttonGap, this.y, this.h, this.h);
      ctx.strokeRect(this.x + this.w / 2 + buttonGap, this.y, this.h, this.h);

      if (
        boolSettings[this.id] ||
        constraints[cID(this.id)] ||
        (constraints[cID(this.id.substring(0, this.id.length - 1))] &&
          constraints[cID(this.id.substring(0, this.id.length - 1))]
            .negative) ||
        (this.id === "DisableHC" && disableHC)
      ) {
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = this.h * 0.125;
        ctx.beginPath();
        ctx.moveTo(
          this.x + this.w / 2 + buttonGap + 7,
          this.y + this.h * (2 / 3)
        );
        ctx.lineTo(
          this.x + this.w / 2 + buttonGap + this.h / 3,
          this.y + this.h - 7
        );
        ctx.lineTo(this.x + this.w / 2 + buttonGap + this.h - 7, this.y + 7);
        ctx.stroke();
      }
    }
  };

  this.showTooltip = function () {
    ctx.textAlign = "left";
    ctx.font = "20px Verdana";
    if (descriptions[this.id] && this.hovering()) {
      const descriptionW =
        Math.max(
          ...descriptions[this.id].map((b) => ctx.measureText(b).width)
        ) + 10;
      const descriptionH = descriptions[this.id].length * 20 + 7.5;
      ctx.lineWidth = 4;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#202020" : "#F8F8F8";
      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#000000" : "#000000";
      ctx.fillRect(mouseX, mouseY - descriptionH, descriptionW, descriptionH);
      ctx.strokeRect(mouseX, mouseY - descriptionH, descriptionW, descriptionH);

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      for (var b = 0; b < descriptions[this.id].length; b++)
        ctx.fillText(
          descriptions[this.id][b],
          mouseX + 5,
          mouseY - descriptionH + 20 * (b + 1)
        );
    }
    ctx.textAlign = "center";
  };
};
