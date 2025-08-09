text = function (cells) {
  this.cells = cells;

  this.fontC = cosmetics[cID("Text")].fontC;
  this.size = cosmetics[cID("Text")].size;
  this.angle = cosmetics[cID("Text")].angle;

  this.value = "";

  this.x = function () {
    return (
      this.cells.map((a) => a.x + cellSL / 2).reduce((a, b) => a + b) /
      this.cells.length
    );
  };

  this.y = function () {
    return (
      this.cells.map((a) => a.y + cellSL / 2).reduce((a, b) => a + b) /
      this.cells.length
    );
  };

  this.show = function () {
    ctx.save();
    ctx.translate(this.x(), this.y());
    ctx.rotate(this.angle * (Math.PI / 180));

    ctx.fillStyle = boolSettings["Dark Mode"]
      ? invertBrightnessFromHex(this.fontC)
      : this.fontC;
    ctx.font = cellSL * 0.8 * this.size + "px Arial";
    ctx.fillText(
      this.value.length ? this.value : "-",
      0,
      cellSL * 0.3 * this.size
    );

    ctx.restore();
  };

  this.type = function (ch) {
    if (this.value.length < 8) this.value += ch;
  };
};

circle = function (cells) {
  this.cells = cells;

  this.baseC = cosmetics[cID("Circle")].baseC;
  this.outlineC = cosmetics[cID("Circle")].outlineC;
  this.fontC = cosmetics[cID("Circle")].fontC;
  this.width = cosmetics[cID("Circle")].width;
  this.height = cosmetics[cID("Circle")].height;
  this.angle = cosmetics[cID("Circle")].angle;

  this.value = "";

  this.x = function () {
    return (
      this.cells.map((a) => a.x + cellSL / 2).reduce((a, b) => a + b) /
      this.cells.length
    );
  };

  this.y = function () {
    return (
      this.cells.map((a) => a.y + cellSL / 2).reduce((a, b) => a + b) /
      this.cells.length
    );
  };

  this.show = function () {
    ctx.save();
    ctx.translate(this.x(), this.y());
    ctx.rotate(this.angle * (Math.PI / 180));

    ctx.lineWidth = lineWT;
    ctx.fillStyle = boolSettings["Dark Mode"]
      ? invertBrightnessFromHex(this.baseC)
      : this.baseC;
    ctx.strokeStyle = this.outlineC;
    ctx.beginPath();
    ctx.ellipse(
      0,
      0,
      (cellSL * this.width) / 2,
      (cellSL * this.height) / 2,
      0,
      0,
      Math.PI * 2
    );
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = boolSettings["Dark Mode"]
      ? invertBrightnessFromHex(this.fontC)
      : this.fontC;
    const fontSize = Math.min(40, (cellSL * this.width) / this.value.length);
    ctx.font = fontSize + "px Arial";
    ctx.fillText(this.value, 0, fontSize * 0.4);

    ctx.restore();
  };

  this.type = function (ch) {
    if (this.value.length < 8) this.value += ch;
  };
};

rectangle = function (cells) {
  this.cells = cells;

  this.baseC = cosmetics[cID("Rectangle")].baseC;
  this.outlineC = cosmetics[cID("Rectangle")].outlineC;
  this.fontC = cosmetics[cID("Rectangle")].fontC;
  this.width = cosmetics[cID("Rectangle")].width;
  this.height = cosmetics[cID("Rectangle")].height;
  this.angle = cosmetics[cID("Rectangle")].angle;

  this.value = "";

  this.x = function () {
    return (
      this.cells.map((a) => a.x + cellSL / 2).reduce((a, b) => a + b) /
      this.cells.length
    );
  };

  this.y = function () {
    return (
      this.cells.map((a) => a.y + cellSL / 2).reduce((a, b) => a + b) /
      this.cells.length
    );
  };

  this.show = function () {
    ctx.save();
    ctx.translate(this.x(), this.y());
    ctx.rotate(this.angle * (Math.PI / 180));

    ctx.lineWidth = lineWT;
    ctx.fillStyle = boolSettings["Dark Mode"]
      ? invertBrightnessFromHex(this.baseC)
      : this.baseC;
    ctx.strokeStyle = this.outlineC;
    ctx.fillRect(
      (-cellSL * this.width) / 2,
      (-cellSL * this.height) / 2,
      cellSL * this.width,
      cellSL * this.height
    );
    ctx.strokeRect(
      (-cellSL * this.width) / 2,
      (-cellSL * this.height) / 2,
      cellSL * this.width,
      cellSL * this.height
    );

    ctx.fillStyle = boolSettings["Dark Mode"]
      ? invertBrightnessFromHex(this.fontC)
      : this.fontC;
    const fontSize = Math.min(40, (cellSL * this.width) / this.value.length);
    ctx.font = fontSize + "px Arial";
    ctx.fillText(this.value, 0, fontSize * 0.4);

    ctx.restore();
  };

  this.type = function (ch) {
    if (this.value.length < 8) this.value += ch;
  };
};

line = function (cell) {
  this.lines = [[cell]];

  this.outlineC = cosmetics[cID("Line")].outlineC;
  this.width = cosmetics[cID("Line")].width;

  this.show = function () {
    for (var a = 0; a < this.lines.length; a++) {
      ctx.lineWidth = (cellSL / 2) * this.width;
      ctx.fillStyle = this.outlineC;
      ctx.strokeStyle = this.outlineC;
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

cage = function (cell) {
  this.cells = [cell];

  this.outlineC = cosmetics[cID("Cage")].outlineC;
  this.fontC = cosmetics[cID("Cage")].fontC;

  this.value = "";

  this.show = function () {
    ctx.lineWidth = lineWT;
    ctx.strokeStyle = this.outlineC;
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

    ctx.fillStyle = boolSettings["Dark Mode"]
      ? invertBrightnessFromHex(this.fontC)
      : this.fontC;
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
    this.cells.push(cell);
    this.sortCells();
  };

  this.sortCells = function () {
    this.cells.sort((a, b) => a.j - b.j);
    this.cells.sort((a, b) => a.i - b.i);
  };

  this.type = function (ch) {
    if (this.value.length < 8) this.value += ch;
  };
};
