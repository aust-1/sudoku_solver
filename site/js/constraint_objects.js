extraregion = function (cell) {
  this.cells = [cell];

  this.show = function () {
    ctx.lineWidth = cellSL * 0.3;
    ctx.fillStyle = ctx.strokeStyle = boolSettings["Dark Mode"]
      ? "#303030"
      : "#E0E0E0";

    for (var a = 0; a < this.cells.length; a++) {
      ctx.fillRect(
        this.cells[a].x + cellSL * 0.1,
        this.cells[a].y + cellSL * 0.1,
        cellSL * 0.8,
        cellSL * 0.8
      );

      for (var b = 0; b < 4; b++) {
        ctx.save();
        ctx.translate(
          this.cells[a].x + cellSL / 2,
          this.cells[a].y + cellSL / 2
        );
        ctx.rotate((b * Math.PI) / 2);

        if (
          (b === 0 &&
            grid[this.cells[a].i - 1] &&
            this.cells.includes(grid[this.cells[a].i - 1][this.cells[a].j])) ||
          (b === 1 &&
            grid[this.cells[a].i][this.cells[a].j + 1] &&
            this.cells.includes(grid[this.cells[a].i][this.cells[a].j + 1])) ||
          (b === 2 &&
            grid[this.cells[a].i + 1] &&
            this.cells.includes(grid[this.cells[a].i + 1][this.cells[a].j])) ||
          (b === 3 &&
            grid[this.cells[a].i][this.cells[a].j - 1] &&
            this.cells.includes(grid[this.cells[a].i][this.cells[a].j - 1]))
        )
          ctx.fillRect(
            -cellSL * 0.4,
            -cellSL / 2,
            cellSL * 0.8,
            cellSL * 0.1 + 1
          );

        if (
          (b === 0 &&
            grid[this.cells[a].i - 1] &&
            grid[this.cells[a].i - 1][this.cells[a].i + 1] &&
            this.cells.includes(
              grid[this.cells[a].i - 1][this.cells[a].j + 1]
            ) &&
            this.cells.includes(grid[this.cells[a].i][this.cells[a].j + 1]) ===
              this.cells.includes(
                grid[this.cells[a].i - 1][this.cells[a].j]
              )) ||
          (b === 1 &&
            grid[this.cells[a].i + 1] &&
            grid[this.cells[a].i + 1][this.cells[a].j + 1] &&
            this.cells.includes(
              grid[this.cells[a].i + 1][this.cells[a].j + 1]
            ) &&
            this.cells.includes(grid[this.cells[a].i][this.cells[a].j + 1]) ===
              this.cells.includes(
                grid[this.cells[a].i + 1][this.cells[a].j]
              )) ||
          (b === 2 &&
            grid[this.cells[a].i + 1] &&
            grid[this.cells[a].i + 1][this.cells[a].j - 1] &&
            this.cells.includes(
              grid[this.cells[a].i + 1][this.cells[a].j - 1]
            ) &&
            this.cells.includes(grid[this.cells[a].i][this.cells[a].j - 1]) ===
              this.cells.includes(
                grid[this.cells[a].i + 1][this.cells[a].j]
              )) ||
          (b === 3 &&
            grid[this.cells[a].i - 1] &&
            grid[this.cells[a].i - 1][this.cells[a].j - 1] &&
            this.cells.includes(
              grid[this.cells[a].i - 1][this.cells[a].j - 1]
            ) &&
            this.cells.includes(grid[this.cells[a].i][this.cells[a].j - 1]) ===
              this.cells.includes(grid[this.cells[a].i - 1][this.cells[a].j]))
        ) {
          ctx.beginPath();
          ctx.moveTo(0, 0);
          ctx.lineTo(cellSL, -cellSL);
          ctx.stroke();
        }

        ctx.restore();
      }
    }
  };

  this.addCellToRegion = function (cell) {
    if (this.cells.length < size) {
      this.cells.push(cell);
      this.sortCells();
    }
  };

  this.sortCells = function () {
    this.cells.sort((a, b) => a.j - b.j);
    this.cells.sort((a, b) => a.i - b.i);
  };
};

odd = function (cells) {
  if (cells) this.cell = cells[0];

  this.show = function () {
    ctx.fillStyle = "#000000";
    ctx.globalAlpha = 0.15;
    ctx.beginPath();
    ctx.arc(
      this.cell.x + cellSL / 2,
      this.cell.y + cellSL / 2,
      cellSL * 0.4,
      0,
      Math.PI * 2
    );
    ctx.fill();
    ctx.globalAlpha = 1.0;
  };
};

even = function (cells) {
  if (cells) this.cell = cells[0];

  this.show = function () {
    ctx.fillStyle = "#000000";
    ctx.globalAlpha = 0.15;
    ctx.fillRect(
      this.cell.x + cellSL * 0.1,
      this.cell.y + cellSL * 0.1,
      cellSL - cellSL * 0.2,
      cellSL - cellSL * 0.2
    );
    ctx.globalAlpha = 1.0;
  };
};

thermometer = function (cell) {
  this.lines = [[cell]];

  this.show = function () {
    for (var a = 0; a < this.lines.length; a++) {
      ctx.lineWidth = cellSL * 0.3;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#707070" : "#D0D0D0";
      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#707070" : "#D0D0D0";
      ctx.beginPath();
      ctx.arc(
        this.lines[a][0].x + cellSL / 2,
        this.lines[a][0].y + cellSL / 2,
        cellSL * 0.4,
        0,
        Math.PI * 2
      );
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(
        this.lines[a][0].x + cellSL / 2,
        this.lines[a][0].y + cellSL / 2
      );
      for (var b = 1; b < this.lines[a].length; b++)
        ctx.lineTo(
          this.lines[a][b].x + cellSL / 2,
          this.lines[a][b].y + cellSL / 2
        );
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(
        this.lines[a][this.lines[a].length - 1].x + cellSL / 2,
        this.lines[a][this.lines[a].length - 1].y + cellSL / 2,
        ctx.lineWidth / 2,
        0,
        Math.PI * 2
      );
      ctx.fill();
    }
  };

  this.addCellToLine = function (cell) {
    if (this.lines[this.lines.length - 1].length < size)
      this.lines[this.lines.length - 1].push(cell);
  };
};

/*
slowthermometer = function(cell){
	this.lines = [[cell]];

	this.show = function(){
		for(var i = 0; i < 2; i++){
			for(var a = 0; a < this.lines.length; a++){
				ctx.lineWidth = cellSL * (i ? 0.1 : 0.3);
				if(i){
					ctx.fillStyle = boolSettings['Dark Mode'] ? '#505050' : '#B0B0B0';
					ctx.strokeStyle = boolSettings['Dark Mode'] ? '#505050' : '#B0B0B0';
				} else {
					ctx.fillStyle = boolSettings['Dark Mode'] ? '#707070' : '#D0D0D0';
					ctx.strokeStyle = boolSettings['Dark Mode'] ? '#707070' : '#D0D0D0';
				}
				ctx.beginPath();
				ctx.arc(this.lines[a][0].x + cellSL/2, this.lines[a][0].y + cellSL/2, cellSL * (i ? 0.3 : 0.4), 0, Math.PI*2);
				ctx.fill();
				ctx.beginPath();
				ctx.moveTo(this.lines[a][0].x + cellSL/2, this.lines[a][0].y + cellSL/2);
				for(var b = 1; b < this.lines[a].length; b++)
					ctx.lineTo(this.lines[a][b].x + cellSL/2, this.lines[a][b].y + cellSL/2);
				ctx.stroke();
				ctx.beginPath();
				ctx.arc(this.lines[a][this.lines[a].length - 1].x + cellSL/2, this.lines[a][this.lines[a].length - 1].y + cellSL/2, ctx.lineWidth/2, 0, Math.PI*2);
				ctx.fill();
			}
		}
	}

	this.addCellToLine = function(cell){
		this.lines[this.lines.length - 1].push(cell);
	}
}
*/

palindrome = function (cell) {
  this.lines = [[cell]];

  this.considered = false;

  this.show = function () {
    for (var a = 0; a < this.lines.length; a++) {
      ctx.lineWidth = cellSL * 0.25;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#606060" : "#C0C0C0";
      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#606060" : "#C0C0C0";
      ctx.beginPath();
      ctx.arc(
        this.lines[a][0].x + cellSL / 2,
        this.lines[a][0].y + cellSL / 2,
        ctx.lineWidth / 2,
        0,
        Math.PI * 2
      );
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(
        this.lines[a][0].x + cellSL / 2,
        this.lines[a][0].y + cellSL / 2
      );
      for (var b = 1; b < this.lines[a].length; b++)
        ctx.lineTo(
          this.lines[a][b].x + cellSL / 2,
          this.lines[a][b].y + cellSL / 2
        );
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(
        this.lines[a][this.lines[a].length - 1].x + cellSL / 2,
        this.lines[a][this.lines[a].length - 1].y + cellSL / 2,
        ctx.lineWidth / 2,
        0,
        Math.PI * 2
      );
      ctx.fill();
    }
  };

  this.addCellToLine = function (cell) {
    this.lines[this.lines.length - 1].push(cell);
  };
};

killercage = function (cell) {
  this.cells = [cell];

  this.value = "";
  this.sums = [];

  this.show = function () {
    ctx.lineWidth = lineWT;
    ctx.strokeStyle = boolSettings["Dark Mode"] ? "#C0C0C0" : "#000000";
    ctx.setLineDash([(cellSL * 0.44) / 3.5, (cellSL * 0.44) / 3.5]);

    for (var a = 0; a < this.cells.length; a++) {
      for (var b = 0; b < 4; b++) {
        ctx.save();
        ctx.translate(
          this.cells[a].x + cellSL / 2,
          this.cells[a].y + cellSL / 2
        );
        ctx.rotate((b * Math.PI) / 2);

        if (
          (b === 0 &&
            (!grid[this.cells[a].i - 1] ||
              !this.cells.includes(
                grid[this.cells[a].i - 1][this.cells[a].j]
              ))) ||
          (b === 1 &&
            (!grid[this.cells[a].i][this.cells[a].j + 1] ||
              !this.cells.includes(
                grid[this.cells[a].i][this.cells[a].j + 1]
              ))) ||
          (b === 2 &&
            (!grid[this.cells[a].i + 1] ||
              !this.cells.includes(
                grid[this.cells[a].i + 1][this.cells[a].j]
              ))) ||
          (b === 3 &&
            (!grid[this.cells[a].i][this.cells[a].j - 1] ||
              !this.cells.includes(grid[this.cells[a].i][this.cells[a].j - 1])))
        ) {
          ctx.beginPath();
          ctx.moveTo(-cellSL * 0.44 - ctx.lineWidth / 2 + 1, -cellSL * 0.44);
          ctx.lineTo(cellSL * 0.44 + ctx.lineWidth / 2 - 1, -cellSL * 0.44);
          ctx.stroke();
        }

        ctx.restore();
      }
    }

    ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
    ctx.font = cellSL * 0.18 + "px Verdana";
    ctx.textAlign = "left";
    ctx.fillText(
      this.value,
      this.cells[0].x + cellSL * 0.111,
      this.cells[0].y + cellSL * 0.2468
    );
    ctx.textAlign = "center";

    ctx.setLineDash([]);
  };

  this.addCellToRegion = function (cell) {
    if (this.cells.length < size) {
      this.cells.push(cell);
      this.sortCells();
    }
  };

  this.sortCells = function () {
    this.cells.sort((a, b) => a.j - b.j);
    this.cells.sort((a, b) => a.i - b.i);
  };

  this.typeNumber = function (num) {
    if (
      (parseInt(num) !== 0 || this.value.length) &&
      parseInt(this.value + String(num)) <= maxInNCells(size)
    )
      this.value += String(num);
  };
};

littlekillersum = function (cells) {
  if (cells) this.cell = cells[0];
  this.direction = null;
  this.cells = null;

  this.value = "";

  this.show = function () {
    ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
    ctx.font = cellSL * 0.6 + "px Arial";
    ctx.fillText(
      this.value.length ? this.value : "-",
      this.cell.x + cellSL / 2,
      this.cell.y + cellSL * 0.75
    );

    ctx.save();
    ctx.translate(this.cell.x + cellSL / 2, this.cell.y + cellSL / 2);
    ctx.rotate(
      (Math.PI / 2) * ["UR", "DR", "DL", "UL"].indexOf(this.direction)
    );

    ctx.strokeStyle = "#000000";
    ctx.lineWidth = cellSL * 0.05;
    ctx.beginPath();
    ctx.moveTo(cellSL * 0.3, -cellSL * 0.3);
    ctx.lineTo(cellSL * 0.45, -cellSL * 0.45);
    ctx.moveTo(cellSL * 0.45, -cellSL * 0.3);
    ctx.lineTo(cellSL * 0.45, -cellSL * 0.45);
    ctx.lineTo(cellSL * 0.3, -cellSL * 0.45);
    ctx.stroke();

    ctx.restore();
  };

  this.updateSet = function () {
    if (this.cell) {
      if (!this.direction) {
        if (this.cell.i < 0) {
          if (adjustedX(mouseX) < this.cell.x + cellSL / 2)
            this.direction = "DL";
          else this.direction = "DR";
        }
        if (this.cell.i >= size) {
          if (adjustedX(mouseX) < this.cell.x + cellSL / 2)
            this.direction = "UL";
          else this.direction = "UR";
        }
        if (this.cell.j < 0) {
          if (adjustedY(mouseY) < this.cell.y + cellSL / 2)
            this.direction = "UR";
          else this.direction = "DR";
        }
        if (this.cell.j >= size) {
          if (adjustedY(mouseY) < this.cell.y + cellSL / 2)
            this.direction = "UL";
          else this.direction = "DL";
        }
      }

      do {
        if (this.cells && !this.cells.length) {
          const directions = ["UR", "DR", "DL", "UL"];
          this.direction =
            directions[
              (directions.indexOf(this.direction) + 1) % directions.length
            ];
        }

        this.cells = [];
        var i = this.cell.i;
        var j = this.cell.j;
        do {
          if (["UL", "UR"].includes(this.direction)) i--;
          else i++;
          if (["UL", "DL"].includes(this.direction)) j--;
          else j++;

          if (i >= 0 && i < size && j >= 0 && j < size)
            this.cells.push(grid[i][j]);
          else break;
        } while (true);
      } while (!this.cells.length);
    }
  };
  this.updateSet();

  this.typeNumber = function (num) {
    if (
      (parseInt(num) !== 0 || this.value.length) &&
      parseInt(this.value + String(num)) <= Math.pow(size, 2)
    )
      this.value += String(num);
  };

  this.minSum = function (exclude) {
    var sum = 0;
    for (var a = 0; a < this.cells.length; a++) {
      if (a !== exclude) {
        if (this.cells[a].value) sum += this.cells[a].value;
        else sum += this.cells[a].candidates[0];
      }
    }

    return sum;
  };

  this.maxSum = function (exclude) {
    var sum = 0;
    for (var a = 0; a < this.cells.length; a++) {
      if (a !== exclude) {
        if (this.cells[a].value) sum += this.cells[a].value;
        else
          sum += this.cells[a].candidates[this.cells[a].candidates.length - 1];
      }
    }

    return sum;
  };
};

sandwichsum = function (cells) {
  if (cells) this.cell = cells[0];
  this.set = null;
  this.location = null;

  this.value = "";
  this.sums = [];

  this.show = function () {
    ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
    ctx.font = cellSL * 0.7 + "px Arial";
    ctx.fillText(
      this.value.length ? this.value : "-",
      this.cell.x + cellSL / 2,
      this.cell.y + cellSL * 0.75
    );
  };

  this.updateSet = function () {
    if (this.cell) {
      if (this.cell.i >= 0 && this.cell.i < size) {
        this.set = getCellsInRow(this.cell.i);
        this.location = "row " + (this.cell.i + 1);
      }
      if (this.cell.j >= 0 && this.cell.j < size) {
        this.set = getCellsInColumn(this.cell.j);
        this.location = "column " + (this.cell.j + 1);
      }
    }
  };
  this.updateSet();

  this.typeNumber = function (num) {
    if (
      this.value !== "0" &&
      parseInt(this.value + String(num)) <= maxInNCells(size) - 1 - size
    )
      this.value += String(num);
  };

  this.getEnds = function () {
    return this.set
      .filter(
        (a) =>
          [1, size].includes(a.value) ||
          (a.candidates.length &&
            a.candidates.every((b) => [1, size].includes(b)))
      )
      .map((a) => this.set.indexOf(a));
  };
};

difference = function (cells) {
  if (cells) this.cells = cells;

  this.value = "";

  this.x = function () {
    return (this.cells[0].x + this.cells[1].x) / 2 + cellSL / 2;
  };

  this.y = function () {
    return (this.cells[0].y + this.cells[1].y) / 2 + cellSL / 2;
  };

  this.show = function () {
    ctx.lineWidth = lineWT;
    ctx.fillStyle = boolSettings["Dark Mode"] ? "#606060" : "#FFFFFF";
    ctx.strokeStyle = "#000000";
    if (
      constraints[cID("Nonconsecutive")] &&
      constraints[cID("Difference")].every((a) =>
        ["", "1"].includes(a.value)
      ) &&
      !constraints[cID("Ratio")].length &&
      !constraints[cID("Ratio")].negative
    ) {
      if (this.cells[0].i === this.cells[1].i) {
        ctx.fillRect(
          this.x() - cellSL * 0.075,
          this.y() - cellSL * 0.4,
          cellSL * 0.15,
          cellSL * 0.8
        );
        ctx.strokeRect(
          this.x() - cellSL * 0.075,
          this.y() - cellSL * 0.4,
          cellSL * 0.15,
          cellSL * 0.8
        );
      }
      if (this.cells[0].j === this.cells[1].j) {
        ctx.fillRect(
          this.x() - cellSL * 0.4,
          this.y() - cellSL * 0.075,
          cellSL * 0.8,
          cellSL * 0.15
        );
        ctx.strokeRect(
          this.x() - cellSL * 0.4,
          this.y() - cellSL * 0.075,
          cellSL * 0.8,
          cellSL * 0.15
        );
      }
    } else {
      ctx.beginPath();
      ctx.arc(this.x(), this.y(), cellSL * 0.1555, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = cellSL * 0.17 + "px Arial";
      ctx.fillText(this.value, this.x(), this.y() + cellSL * 0.06789);
    }
  };

  this.typeNumber = function (num) {
    if (
      (parseInt(num) !== 0 || this.value.length) &&
      parseInt(this.value + String(num)) <= size - 1
    )
      this.value += String(num);
  };
};

ratio = function (cells) {
  if (cells) this.cells = cells;

  this.value = "";

  this.x = function () {
    return (this.cells[0].x + this.cells[1].x) / 2 + cellSL / 2;
  };

  this.y = function () {
    return (this.cells[0].y + this.cells[1].y) / 2 + cellSL / 2;
  };

  this.show = function () {
    ctx.lineWidth = lineWT;
    ctx.fillStyle = "#000000";
    ctx.strokeStyle = "#000000";
    ctx.beginPath();
    ctx.arc(this.x(), this.y(), cellSL * 0.1555, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#FFFFFF";
    ctx.font = cellSL * 0.17 + "px Arial";
    ctx.fillText(this.value, this.x(), this.y() + cellSL * 0.06789);
  };

  this.typeNumber = function (num) {
    if (
      (parseInt(num) !== 0 || this.value.length) &&
      parseInt(this.value + String(num)) <= size
    )
      this.value += String(num);
  };
};

clone = function (cell) {
  this.cells = [cell];
  this.cloneCells = [cell];

  this.considered = false;

  this.show = function () {
    ctx.fillStyle = "#000000";
    ctx.strokeStyle = "#000000";

    for (var a = 0; a < this.cells.length; a++) {
      ctx.globalAlpha = 0.15;
      ctx.fillRect(this.cells[a].x, this.cells[a].y, cellSL, cellSL);
      ctx.fillRect(this.cloneCells[a].x, this.cloneCells[a].y, cellSL, cellSL);
      ctx.globalAlpha = 1.0;

      if (!previewMode && currentTool === "Clone") {
        ctx.globalAlpha = 0.05;
        ctx.fillStyle = "#000000";
        ctx.beginPath();
        ctx.arc(
          this.cloneCells[a].x + cellSL / 2,
          this.cloneCells[a].y + cellSL / 2,
          cellSL * 0.3,
          0,
          Math.PI * 2
        );
        ctx.fill();
        ctx.globalAlpha = 1.0;
      }
    }
  };

  this.addCellToRegion = function (cell) {
    this.cells.push(cell);
    this.cloneCells.push(cell);
    this.sortCells();
  };

  this.sortCells = function () {
    this.cells.sort((a, b) => a.j - b.j);
    this.cells.sort((a, b) => a.i - b.i);
    this.cloneCells.sort((a, b) => a.j - b.j);
    this.cloneCells.sort((a, b) => a.i - b.i);
  };
};

arrow = function (cell) {
  this.cells = [cell];
  this.lines = [];

  this.show = function () {
    ctx.fillStyle = highlightCs[0];

    ctx.lineWidth = cellSL * (0.71 + 0.085 * 2);
    ctx.strokeStyle = boolSettings["Dark Mode"] ? "#606060" : "#A0A0A0";
    for (var a = 1; a < this.cells.length; a++) {
      ctx.beginPath();
      ctx.moveTo(
        this.cells[a - 1].x + cellSL / 2,
        this.cells[a - 1].y + cellSL / 2
      );
      ctx.lineTo(this.cells[a].x + cellSL / 2, this.cells[a].y + cellSL / 2);
      ctx.stroke();
    }
    ctx.lineWidth = cellSL * 0.085;
    ctx.strokeStyle = boolSettings["Dark Mode"] ? "#606060" : "#A0A0A0";
    for (var a = 0; a < this.lines.length; a++) {
      if (this.lines[a].length > 1) {
        ctx.beginPath();
        ctx.moveTo(
          this.lines[a][0].x + cellSL / 2,
          this.lines[a][0].y + cellSL / 2
        );
        ctx.lineTo(
          this.lines[a][1].x + cellSL / 2,
          this.lines[a][1].y + cellSL / 2
        );
        ctx.stroke();
      }
    }
    for (var a = 0; a < this.cells.length; a++) {
      ctx.beginPath();
      ctx.arc(
        this.cells[a].x + cellSL / 2,
        this.cells[a].y + cellSL / 2,
        cellSL * 0.4,
        0,
        Math.PI * 2
      );
      ctx.fill();
      ctx.stroke();
    }
    ctx.lineWidth = cellSL * 0.71;
    ctx.strokeStyle = highlightCs[0];
    for (var a = 1; a < this.cells.length; a++) {
      ctx.beginPath();
      ctx.moveTo(
        this.cells[a - 1].x + cellSL / 2,
        this.cells[a - 1].y + cellSL / 2
      );
      ctx.lineTo(this.cells[a].x + cellSL / 2, this.cells[a].y + cellSL / 2);
      ctx.stroke();
    }
    ctx.lineWidth = cellSL * 0.085;
    ctx.strokeStyle = boolSettings["Dark Mode"] ? "#606060" : "#A0A0A0";
    for (var a = 0; a < this.lines.length; a++) {
      if (this.lines[a].length > 1) {
        ctx.beginPath();
        ctx.moveTo(
          (this.lines[a][0].x + this.lines[a][1].x * 9) / 10 + cellSL / 2,
          (this.lines[a][0].y + this.lines[a][1].y * 9) / 10 + cellSL / 2
        );
        for (var b = 1; b < this.lines[a].length; b++)
          ctx.lineTo(
            this.lines[a][b].x + cellSL / 2,
            this.lines[a][b].y + cellSL / 2
          );
        ctx.stroke();
        if (this.lines[a].length > 1) {
          const prevX = this.lines[a][this.lines[a].length - 2].x;
          const prevY = this.lines[a][this.lines[a].length - 2].y;
          const lastX = this.lines[a][this.lines[a].length - 1].x;
          const lastY = this.lines[a][this.lines[a].length - 1].y;
          const angle = Math.atan2(prevY - lastY, prevX - lastX);
          ctx.save();
          ctx.translate(lastX + cellSL / 2, lastY + cellSL / 2);
          ctx.rotate(angle);
          ctx.beginPath();
          ctx.moveTo(cellSL * 0.3, cellSL * 0.3);
          ctx.lineTo(0, 0);
          ctx.lineTo(cellSL * 0.3, -cellSL * 0.3);
          ctx.stroke();
          ctx.restore();
        }
      }
    }
  };

  this.addCellToRegion = function (cell) {
    this.cells.push(cell);
    this.sortCells();
  };

  this.addCellToLine = function (cell) {
    this.lines[this.lines.length - 1].push(cell);
  };

  this.sortCells = function () {
    this.cells.sort((a, b) => a.j - b.j);
    this.cells.sort((a, b) => a.i - b.i);
  };

  this.minValue = function (test, exclude) {
    var value = "";
    for (var a = 0; a < this.cells.length; a++) {
      if (a === exclude) value += test;
      else {
        if (this.cells[a].value) value += this.cells[a].value;
        else value += this.cells[a].candidates[0];
      }
    }

    return value;
  };

  this.maxValue = function (test, exclude) {
    var value = "";
    for (var a = 0; a < this.cells.length; a++) {
      if (a === exclude) value += test;
      else {
        if (this.cells[a].value) value += this.cells[a].value;
        else
          value +=
            this.cells[a].candidates[this.cells[a].candidates.length - 1];
      }
    }

    return value;
  };

  this.minSum = function (index, exclude) {
    var sum = 0;
    for (var a = 1; a < this.lines[index].length; a++) {
      if (a !== exclude) {
        if (this.lines[index][a].value) sum += this.lines[index][a].value;
        else sum += this.lines[index][a].candidates[0];
      }
    }

    return sum;
  };

  this.maxSum = function (index, exclude) {
    var sum = 0;
    for (var a = 1; a < this.lines[index].length; a++) {
      if (a !== exclude) {
        if (this.lines[index][a].value) sum += this.lines[index][a].value;
        else
          sum +=
            this.lines[index][a].candidates[
              this.lines[index][a].candidates.length - 1
            ];
      }
    }

    return sum;
  };
};

betweenline = function (cell) {
  this.lines = [[cell]];

  this.minCell = null;
  this.maxCell = null;

  this.show = function () {
    for (var a = 0; a < this.lines.length; a++) {
      ctx.lineWidth = cellSL * 0.075;

      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#707070" : "#9A9A9A";
      ctx.beginPath();
      ctx.moveTo(
        this.lines[a][0].x + cellSL / 2,
        this.lines[a][0].y + cellSL / 2
      );
      for (var b = 1; b < this.lines[a].length; b++)
        ctx.lineTo(
          this.lines[a][b].x + cellSL / 2,
          this.lines[a][b].y + cellSL / 2
        );
      ctx.stroke();

      ctx.fillStyle = boolSettings["Dark Mode"] ? "#888888" : "#EAEAEA";
      for (
        var b = 0, i = 0;
        b < this.lines[a].length && (this.lines[a].length > 1 || !i);
        b += this.lines[a].length - 1, i++
      ) {
        ctx.beginPath();
        ctx.arc(
          this.lines[a][b].x + cellSL / 2,
          this.lines[a][b].y + cellSL / 2,
          cellSL / 2 - ctx.lineWidth / 2,
          0,
          Math.PI * 2
        );
        ctx.fill();
        ctx.stroke();
      }
    }
  };

  this.addCellToLine = function (cell) {
    this.lines[this.lines.length - 1].push(cell);
  };
};

minimum = function (cells) {
  if (cells) this.cell = cells[0];

  this.show = function () {
    ctx.fillStyle = "#000000";
    ctx.globalAlpha = 0.2;
    ctx.fillRect(this.cell.x, this.cell.y, cellSL, cellSL);
    ctx.globalAlpha = 1.0;

    ctx.lineWidth = cellSL * 0.03;
    ctx.strokeStyle = "#000000";
    ctx.save();
    ctx.translate(this.cell.x + cellSL / 2, this.cell.y + cellSL / 2);
    for (var a = 0; a < 4; a++) {
      if (
        (a === 0 &&
          grid[this.cell.i - 1] &&
          constraints[cID("Minimum")].findIndex(
            (b) => b.cell === grid[this.cell.i - 1][this.cell.j]
          ) === -1) ||
        (a === 1 &&
          grid[this.cell.i][this.cell.j + 1] &&
          constraints[cID("Minimum")].findIndex(
            (b) => b.cell === grid[this.cell.i][this.cell.j + 1]
          ) === -1) ||
        (a === 2 &&
          grid[this.cell.i + 1] &&
          constraints[cID("Minimum")].findIndex(
            (b) => b.cell === grid[this.cell.i + 1][this.cell.j]
          ) === -1) ||
        (a === 3 &&
          grid[this.cell.i][this.cell.j - 1] &&
          constraints[cID("Minimum")].findIndex(
            (b) => b.cell === grid[this.cell.i][this.cell.j - 1]
          ) === -1)
      ) {
        ctx.save();
        ctx.rotate((a * Math.PI) / 2);
        ctx.beginPath();
        ctx.moveTo(-cellSL * 0.1, -cellSL * 0.4);
        ctx.lineTo(0, -cellSL * 0.4 + cellSL * 0.05);
        ctx.lineTo(cellSL * 0.1, -cellSL * 0.4);
        ctx.stroke();
        ctx.restore();
      }
    }
    ctx.restore();
  };
};

maximum = function (cells) {
  if (cells) this.cell = cells[0];

  this.show = function () {
    ctx.fillStyle = "#000000";
    ctx.globalAlpha = 0.2;
    ctx.fillRect(this.cell.x, this.cell.y, cellSL, cellSL);
    ctx.globalAlpha = 1.0;

    ctx.lineWidth = cellSL * 0.03;
    ctx.strokeStyle = "#000000";
    ctx.save();
    ctx.translate(this.cell.x + cellSL / 2, this.cell.y + cellSL / 2);
    for (var a = 0; a < 4; a++) {
      if (
        (a === 0 &&
          grid[this.cell.i - 1] &&
          constraints[cID("Maximum")].findIndex(
            (b) => b.cell === grid[this.cell.i - 1][this.cell.j]
          ) === -1) ||
        (a === 1 &&
          grid[this.cell.i][this.cell.j + 1] &&
          constraints[cID("Maximum")].findIndex(
            (b) => b.cell === grid[this.cell.i][this.cell.j + 1]
          ) === -1) ||
        (a === 2 &&
          grid[this.cell.i + 1] &&
          constraints[cID("Maximum")].findIndex(
            (b) => b.cell === grid[this.cell.i + 1][this.cell.j]
          ) === -1) ||
        (a === 3 &&
          grid[this.cell.i][this.cell.j - 1] &&
          constraints[cID("Maximum")].findIndex(
            (b) => b.cell === grid[this.cell.i][this.cell.j - 1]
          ) === -1)
      ) {
        ctx.save();
        ctx.rotate((a * Math.PI) / 2);
        ctx.beginPath();
        ctx.moveTo(-cellSL * 0.1, -cellSL * 0.4);
        ctx.lineTo(0, -cellSL * 0.4 + -cellSL * 0.05);
        ctx.lineTo(cellSL * 0.1, -cellSL * 0.4);
        ctx.stroke();
        ctx.restore();
      }
    }
    ctx.restore();
  };
};

xv = function (cells) {
  if (cells) this.cells = cells;

  this.value = "";

  this.x = function () {
    return (this.cells[0].x + this.cells[1].x) / 2 + cellSL / 2;
  };

  this.y = function () {
    return (this.cells[0].y + this.cells[1].y) / 2 + cellSL / 2;
  };

  this.show = function () {
    ctx.fillStyle = highlightCs[0];
    ctx.beginPath();
    ctx.arc(this.x(), this.y(), cellSL * 0.2, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
    ctx.font = "bold " + cellSL * 0.35 + "px Arial";
    ctx.fillText(this.value, this.x(), this.y() + cellSL * 0.12345);
  };
};

quadruple = function (cells) {
  if (cells) this.cells = cells;

  this.values = [];

  this.x = function () {
    return (this.cells[0].x + this.cells[3].x) / 2 + cellSL / 2;
  };

  this.y = function () {
    return (this.cells[0].y + this.cells[3].y) / 2 + cellSL / 2;
  };

  this.show = function () {
    ctx.lineWidth = lineWT;
    ctx.fillStyle = boolSettings["Dark Mode"] ? "#606060" : "#FFFFFF";
    ctx.strokeStyle = "#000000";
    ctx.beginPath();
    ctx.arc(this.x(), this.y(), cellSL * 0.25, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
    ctx.font = cellSL * 0.185 + "px Arial";
    if (this.values.length <= 2)
      ctx.fillText(this.values.join(""), this.x(), this.y() + cellSL * 0.06789);
    else {
      ctx.fillText(
        this.values.slice(0, 2).join(" "),
        this.x(),
        this.y() + cellSL * -0.02211
      );
      ctx.fillText(
        this.values.slice(2, Infinity).join(" "),
        this.x(),
        this.y() + cellSL * 0.15789
      );
    }
  };

  this.sortCells = function () {
    this.cells.sort((a, b) => a.j - b.j);
    this.cells.sort((a, b) => a.i - b.i);
  };

  this.typeNumber = function (num) {
    if (num > 0 && this.values.length < 4) {
      if (this.values.indexOf(num) === this.values.lastIndexOf(num)) {
        this.values.push(num);
        this.values.sort();
      }
    }
  };
};
