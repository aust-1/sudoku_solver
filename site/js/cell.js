cell = function (i, j, outside) {
  this.i = i;
  this.j = j;
  this.x = gridX + cellSL * j;
  this.y = gridY + cellSL * i;
  this.outside = outside || false;

  this.region = outside
    ? null
    : Math.floor(i / regionH) * regionH + Math.floor(j / regionW);

  this.value = 0;
  this.valueBackup = 0;

  this.given = false;

  this.candidates = [];
  this.candidatesBackup = [];

  this.cornerPencilMarks = [];
  this.centerPencilMarks = [];
  this.c = 0;
  this.highlight = 0;

  this.hovering = function (strict) {
    x = adjustedX(mouseX);
    y = adjustedY(mouseY);
    if (strict) {
      const margin = cellSL * 0.2;
      return (
        x > this.x + margin &&
        x < this.x + cellSL - margin &&
        y > this.y + margin &&
        y < this.y + cellSL - margin
      );
    } else
      return (
        x > this.x && x < this.x + cellSL && y > this.y && y < this.y + cellSL
      );
  };

  this.click = function () {
    if (this.hovering()) {
      if (selection.includes(this)) {
        selection.splice(selection.indexOf(this), 1);
        holding = false;
      } else {
        if (
          tools.includes(currentTool) &&
          ((toolConstraints.includes(currentTool) &&
            this.outside === outsideTools.includes(currentTool)) ||
            (toolCosmetics.includes(currentTool) &&
              ((this.outside &&
                outsideTools.includes(currentTool) &&
                cosmeticPlaceMode === "Outside") ||
                (!this.outside &&
                  (!outsideTools.includes(currentTool) ||
                    cosmeticPlaceMode !== "Outside")))))
        ) {
          useTool(this);
        } else if (selectableTools.includes(currentTool) && !this.outside)
          this.select();
      }
    }
  };

  this.showSelection = function () {
    if (!previewMode) {
      if (selection.includes(this)) {
        ctx.fillStyle = boolSettings["Dark Mode"] ? "#FFFFFF" : "#FFFF00";
        ctx.globalAlpha = 0.2;
        ctx.fillRect(this.x, this.y, cellSL, cellSL);
        ctx.globalAlpha = 1.0;
      } else if (cellsSeenBySelection.includes(this)) {
        ctx.fillStyle = boolSettings["Dark Mode"] ? "#FFFFFF" : "#FFFF00";
        ctx.globalAlpha = 0.08;
        ctx.fillRect(this.x, this.y, cellSL, cellSL);
        ctx.globalAlpha = 1.0;
      }
    }
  };

  this.showBottom = function () {
    ctx.fillStyle = highlightCs[this.c];
    ctx.fillRect(this.x, this.y, cellSL, cellSL);
    if (this.highlight) {
      ctx.fillStyle = highlightCs[previewMode ? 0 : this.highlight];
      ctx.fillRect(this.x, this.y, cellSL, cellSL);
    }
  };

  this.showTop = function () {
    if (currentTool === "Regions" && !previewMode) {
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#505050" : "#E0E0E0";
      ctx.font = cellSL * 0.8 + "px Arial";
      ctx.fillText(this.region + 1, this.x + cellSL / 2, this.y + cellSL * 0.8);
    } else if (this.value) {
      if (
        !previewMode &&
        boolSettings["Highlight Conflicts"] &&
        this.value &&
        !candidatePossibleInCell(this.value, this, { bruteForce: true })
      )
        ctx.fillStyle = "#FF0000";
      else {
        if (boolSettings["Dark Mode"])
          ctx.fillStyle = this.given ? "#FFFFFF" : "#B0B0B0";
        else ctx.fillStyle = this.given ? "#000000" : "#505050";
      }

      if (this.given || !previewMode) {
        ctx.font = cellSL * 0.8 + "px Arial";
        ctx.fillText(this.value, this.x + cellSL / 2, this.y + cellSL * 0.8);
      }
    } else {
      if (!previewMode) {
        const TLInterference =
          constraints[cID("Killer Cage")].some(
            (a) => a.value.length && a.cells[0] === this
          ) ||
          cosmetics[cID("Cage")].some(
            (a) => a.value.length && a.cells[0] === this
          ) ||
          constraints[cID("Quadruple")].some((a) => a.cells[3] === this);
        const TRInterference = constraints[cID("Quadruple")].some(
          (a) => a.cells[2] === this
        );
        const BLInterference = constraints[cID("Quadruple")].some(
          (a) => a.cells[1] === this
        );
        const BRInterference = constraints[cID("Quadruple")].some(
          (a) => a.cells[0] === this
        );

        ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
        ctx.font = cellSL * 0.19 + "px Arial";
        for (var a = 0; a < Math.min(4, this.cornerPencilMarks.length); a++) {
          var x = this.x + cellSL * 0.14 + cellSL * 0.7 * (a % 2);
          if ((a === 0 && TLInterference) || (a === 2 && BLInterference))
            x += cellSL * 0.285;
          if ((a === 1 && TRInterference) || (a === 3 && BRInterference))
            x -= cellSL * 0.285;
          var y = this.y + cellSL * 0.25 + cellSL * 0.64 * (a > 1);
          ctx.fillText(this.cornerPencilMarks[a], x, y);
        }

        ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
        ctx.font = cellSL * 0.19 + "px Arial";
        centerPencilMarks = Array(Math.ceil(this.centerPencilMarks.length / 5))
          .fill()
          .map((a, i) => i * 5)
          .map((a) => this.centerPencilMarks.slice(a, a + 5));
        for (var a = 0; a < centerPencilMarks.length; a++)
          ctx.fillText(
            centerPencilMarks[a].join(""),
            this.x + cellSL / 2,
            this.y +
              cellSL * 0.6 -
              ((centerPencilMarks.length - 1) / 2 - a) * cellSL * 0.1666
          );
      }
    }
  };

  this.showOutline = function () {
    ctx.strokeStyle = "#000000";
    for (var a = 0; a < 4; a++) {
      ctx.save();
      ctx.translate(this.x + cellSL / 2, this.y + cellSL / 2);
      ctx.rotate((a * Math.PI) / 2);

      if (
        (a === 0 &&
          (!grid[this.i - 1] ||
            grid[this.i - 1][this.j].region !== grid[this.i][this.j].region)) ||
        (a === 1 &&
          (!grid[this.i][this.j + 1] ||
            grid[this.i][this.j + 1].region !== grid[this.i][this.j].region)) ||
        (a === 2 &&
          (!grid[this.i + 1] ||
            grid[this.i + 1][this.j].region !== grid[this.i][this.j].region)) ||
        (a === 3 &&
          (!grid[this.i][this.j - 1] ||
            grid[this.i][this.j - 1].region !== grid[this.i][this.j].region))
      ) {
        ctx.lineWidth = lineWW;
      } else ctx.lineWidth = lineWT;

      ctx.beginPath();
      ctx.moveTo(-cellSL / 2 - ctx.lineWidth / 2 + 1, -cellSL / 2);
      ctx.lineTo(cellSL / 2 + ctx.lineWidth / 2 - 1, -cellSL / 2);
      ctx.stroke();

      ctx.restore();
    }
  };

  this.select = function () {
    if (!selection.includes(this)) selection.push(this);
  };

  this.enter = function (value, forced) {
    if (!forced || !this.given) {
      value = parseInt(value);

      if (
        forced ||
        !this.given ||
        mode === "Setting" ||
        tempEnterMode === "Highlight"
      ) {
        if (value <= size) {
          if (!value) {
            this.value = 0;
            this.cornerPencilMarks = [];
            this.centerPencilMarks = [];
            this.given = false;
            addAllCandidates(this);
          } else if (forced || tempEnterMode === "Normal") {
            this.value = value;
            this.given = mode === "Setting" && !forced;
            this.cornerPencilMarks = [];
            this.centerPencilMarks = [];
            this.candidates = [value];
          } else if (tempEnterMode === "Corner") {
            if (!this.value) {
              if (this.cornerPencilMarks.includes(value))
                this.cornerPencilMarks.splice(
                  this.cornerPencilMarks.indexOf(value),
                  1
                );
              else this.cornerPencilMarks.push(value);
              this.cornerPencilMarks.sort((a, b) => a - b);
            }
          } else if (tempEnterMode === "Center") {
            if (!this.value) {
              if (this.centerPencilMarks.includes(value))
                this.centerPencilMarks.splice(
                  this.centerPencilMarks.indexOf(value),
                  1
                );
              else this.centerPencilMarks.push(value);
              this.centerPencilMarks.sort((a, b) => a - b);
            }
          }
        }

        if (!forced && tempEnterMode === "Highlight") {
          if (mode === "Setting") {
            this.c = value - 1;
            this.highlight = 0;
          } else if (mode === "Solving") this.highlight = value - 1;
        }
      }
    }
  };
};
