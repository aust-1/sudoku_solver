useTool = function (cell) {
  const tool = constraints[cID(currentTool)] || cosmetics[cID(currentTool)];

  if (!cell.outside) {
    var nearestCells = getCells().sort(
      (a, b) =>
        Math.sqrt(
          Math.pow(a.x + cellSL / 2 - adjustedX(mouseX), 2) +
            Math.pow(a.y + cellSL / 2 - adjustedY(mouseY), 2)
        ) -
        Math.sqrt(
          Math.pow(b.x + cellSL / 2 - adjustedX(mouseX), 2) +
            Math.pow(b.y + cellSL / 2 - adjustedY(mouseY), 2)
        )
    );
    const nearestI =
      nearestCells[
        nearestCells.findIndex(
          (a) => Math.abs(cell.i - a.i) === 1 && cell.j === a.j
        )
      ].i;
    const nearestJ =
      nearestCells[
        nearestCells.findIndex(
          (a) => cell.i === a.i && Math.abs(cell.j - a.j) === 1
        )
      ].j;
    const nearestCells1 = [cell];
    const nearestCells2 = [cell, nearestCells[1]];
    const nearestCells4 = [
      cell,
      grid[cell.i][nearestJ],
      grid[nearestI][cell.j],
      grid[nearestI][nearestJ],
    ];

    if (
      undraggableCosmetics.includes(currentTool) &&
      cosmeticPlaceMode === "Auto"
    ) {
      nearestCells = [nearestCells1, nearestCells2, nearestCells4].map((a) =>
        Math.sqrt(
          Math.pow(
            a.map((b) => b.x + cellSL / 2).reduce((b, c) => b + c) / a.length -
              adjustedX(mouseX),
            2
          ) +
            Math.pow(
              a.map((b) => b.y + cellSL / 2).reduce((b, c) => b + c) /
                a.length -
                adjustedY(mouseY),
              2
            )
        )
      );
      nearestCells = [nearestCells1, nearestCells2, nearestCells4][
        nearestCells.indexOf(Math.min(...nearestCells))
      ];
    } else {
      if (
        oneCellAtATimeTools.includes(currentTool) ||
        (undraggableCosmetics.includes(currentTool) &&
          cosmeticPlaceMode === "Cell")
      )
        nearestCells = nearestCells1;
      if (
        borderConstraints.includes(currentTool) ||
        (undraggableCosmetics.includes(currentTool) &&
          cosmeticPlaceMode === "Border")
      )
        nearestCells = nearestCells2;
      if (
        cornerConstraints.includes(currentTool) ||
        (undraggableCosmetics.includes(currentTool) &&
          cosmeticPlaceMode === "Corner")
      )
        nearestCells = nearestCells4;
    }
  }

  if (draggableTools.includes(currentTool)) {
    var overlapping = null;
    var deleted = false;
    for (var a = 0; a < tool.length; a++) {
      if (tool[a].lines) {
        for (var b = 0; b < tool[a].lines.length; b++) {
          if (tool[a].lines[b].includes(nearestCells[0])) {
            overlapping = "Line";

            if (!shifting) {
              if (currentTool === "Arrow") tool[a].lines.splice(b, 1);
              else tool.splice(a, 1);
              deleted = true;
            }

            break;
          }
        }
        if (overlapping) break;
      }
    }

    for (var a = 0; a < tool.length; a++) {
      if (tool[a].cells) {
        if (
          tool[a].cells.includes(cell) ||
          (tool[a].cloneCells && tool[a].cloneCells.includes(cell))
        ) {
          overlapping = "Region";
          if (tool[a].cloneCells && tool[a].cloneCells.includes(cell))
            dragAnchor = cell;

          if (!shifting) {
            tool.splice(a, 1);
            deleted = true;
          }

          break;
        }
      }
    }

    if (!deleted) {
      changeCancelled = true;

      if (!overlapping || overlapping === "Line") {
        tool.push(new window[cID(currentTool)](cell));
        if (lineTools.includes(currentTool)) dragMode = "Line";
        if (regionTools.includes(currentTool)) dragMode = "Region";
      }

      if (overlapping === "Region") {
        tool.push(
          tool.splice(
            tool.findIndex((b) => b.cells.includes(cell)),
            1
          )[0]
        );
        dragMode = "Region";

        if (currentTool === "Clone" && dragAnchor) dragMode = "Move Clone";

        if (currentTool === "Arrow") {
          tool[tool.length - 1].lines.push([cell]);
          dragMode = "Line";
        }
      }
    } else holding = false;
  }

  if (
    outsideTools.includes(currentTool) &&
    (toolConstraints.includes(currentTool) ||
      (toolCosmetics.includes(currentTool) && cosmeticPlaceMode === "Outside"))
  ) {
    if (
      outsideCornerTools.includes(currentTool) ||
      (cell.i >= 0 && cell.i < size) ||
      (cell.j >= 0 && cell.j < size)
    ) {
      var overlapping = false;
      var deleted = false;
      for (var a = 0; a < outsideTools.length; a++) {
        const tool2 =
          constraints[cID(outsideTools[a])] || cosmetics[cID(outsideTools[a])];
        const index = tool2.findIndex(
          (a) => a.cell === cell || (a.cells && a.cells[0] === cell)
        );
        overlapping = index > -1;
        if (overlapping) {
          if (!shifting && !controlling) {
            tool2.splice(index, 1);
            deleted = true;
          }
          break;
        }
      }

      if (!deleted) {
        if (!overlapping) tool.push(new window[cID(currentTool)]([cell]));
        else
          tool.push(
            tool.splice(
              tool.findIndex((a) => a.cell === cell),
              1
            )[0]
          );
      }
    }
  } else if (
    perCellConstraints.includes(currentTool) ||
    betweenCellConstraints.includes(currentTool) ||
    undraggableCosmetics.includes(currentTool)
  ) {
    var overlapping = false;
    var deleted = false;

    var toolsToCheckForOverlapsWith = null;
    if (toolConstraints.includes(currentTool))
      toolsToCheckForOverlapsWith = perCellConstraints
        .concat(betweenCellConstraints)
        .map((a) => constraints[cID(a)]);
    if (toolCosmetics.includes(currentTool))
      toolsToCheckForOverlapsWith = [tool];

    toolsToCheckForOverlapsWith.forEach((tool2) => {
      const index = tool2.findIndex((a) => {
        return (
          (a.cell && nearestCells.length === 1 && a.cell === nearestCells[0]) ||
          (a.cells &&
            a.cells.length === nearestCells.length &&
            a.cells.length ===
              a.cells.filter((b) => nearestCells.includes(b)).length)
        );
      });
      if (index >= 0) {
        overlapping = true;
        if (!shifting && !controlling) {
          tool2.splice(index, 1);
          deleted = true;
        }
      }
    });

    if (!deleted) {
      if (!overlapping) {
        tool.push(new window[cID(currentTool)](nearestCells));
        if (tool[tool.length - 1].sortCells) tool[tool.length - 1].sortCells();
      } else
        tool.push(
          tool.splice(
            tool.findIndex((a) =>
              nearestCells.every((b) => a.cells.includes(b))
            ),
            1
          )[0]
        );
    }
  }
};

useDraggableTools = function () {
  const tool = constraints[cID(currentTool)] || cosmetics[cID(currentTool)];
  if (draggableTools.includes(currentTool)) {
    const recent = tool[tool.length - 1];
    if (recent.cells) var recentCell = recent.cells[recent.cells.length - 1];
    if (recent.lines) var recentLine = recent.lines[recent.lines.length - 1];

    getCells().forEach((cell) => {
      if (cell.hovering(dragMode !== "Move Clone")) {
        if (dragMode === "Line" && !recentLine.includes(cell)) {
          if (
            (recentLine.length &&
              Math.abs(cell.i - recentLine[recentLine.length - 1].i) <= 1 &&
              Math.abs(cell.j - recentLine[recentLine.length - 1].j) <= 1) ||
            (!recentLine.length &&
              recent.cells &&
              recent.cells.some(
                (a) =>
                  (Math.abs(cell.i - a.i) === 0 &&
                    Math.abs(cell.j - a.j) === 1) ||
                  (Math.abs(cell.i - a.i) === 1 && Math.abs(cell.j - a.j) === 0)
              ))
          )
            recent.addCellToLine(cell);
        }

        if (
          dragMode === "Region" &&
          !tool.some((a) => a.cells.includes(cell))
        ) {
          if (
            (diagonalRegionTools.includes(currentTool) &&
              recent.cells.some(
                (a) =>
                  (Math.abs(cell.i - a.i) <= 1 &&
                    Math.abs(cell.j - a.j) === 1) ||
                  (Math.abs(cell.i - a.i) === 1 && Math.abs(cell.j - a.j) <= 1)
              )) ||
            (!diagonalRegionTools.includes(currentTool) &&
              recent.cells.some(
                (a) =>
                  (Math.abs(cell.i - a.i) === 0 &&
                    Math.abs(cell.j - a.j) === 1) ||
                  (Math.abs(cell.i - a.i) === 1 && Math.abs(cell.j - a.j) === 0)
              ))
          )
            recent.addCellToRegion(cell);
        }

        if (dragMode === "Move Clone") {
          const iOffset = cell.i - dragAnchor.i;
          const jOffset = cell.j - dragAnchor.j;

          if (
            recent.cloneCells.every(
              (a) =>
                a.i + iOffset >= 0 &&
                a.i + iOffset < size &&
                a.j + jOffset >= 0 &&
                a.j + jOffset < size
            )
          ) {
            const cells = [];
            for (var a = 0; a < recent.cells.length; a++)
              cells.push(
                grid[recent.cloneCells[a].i + iOffset][
                  recent.cloneCells[a].j + jOffset
                ]
              );

            recent.cloneCells = [...cells];
            dragAnchor = cell;
          }
        }

        generateCandidates();
      }
    });
  }
};

doneDraggingTool = function () {
  const tool = constraints[cID(currentTool)] || cosmetics[cID(currentTool)];

  if (lineTools.includes(currentTool)) {
    for (var a = tool.length - 1; a >= 0; a--) {
      for (var b = 0; b < tool[a].lines.length; b++) {
        if (tool[a].lines[b].length <= 1) {
          if (currentTool === "Arrow") {
            tool[a].lines.splice(b, 1);
            changeCancelled = true;
            break;
          } else {
            tool.splice(a, 1);
            changeCancelled = true;
            break;
          }
        }
      }
    }
  }

  if (regionTools.includes(currentTool)) {
    for (var a = tool.length - 1; a >= 0; a--) {
      if (currentTool === "Extra Region") {
        if (tool[a].cells.length < size) {
          tool.splice(a, 1);
          changeCancelled = true;
        }
      }
    }
  }
};

typeConstraint = function (c) {
  if (typableConstraints.includes(currentTool)) {
    if (c === "Backspace" || c === "Delete") {
      const constraint =
        constraints[cID(currentTool)][constraints[cID(currentTool)].length - 1];
      if (constraint.value)
        constraint.value = constraint.value.substring(
          0,
          constraint.value.length - 1
        );
      if (constraint.values)
        constraint.values.splice(constraint.values.length - 1, 1);
    } else {
      const constraint =
        constraints[cID(currentTool)][constraints[cID(currentTool)].length - 1];
      if (constraint && constraint.typeNumber) constraint.typeNumber(c);
    }
    return true;
  } else return false;
};

typeCosmetic = function (c) {
  if (toolCosmetics.includes(currentTool)) {
    if (c === "Backspace" || c === "Delete")
      cosmetics[cID(currentTool)][
        cosmetics[cID(currentTool)].length - 1
      ].value = cosmetics[cID(currentTool)][
        cosmetics[cID(currentTool)].length - 1
      ].value.substring(
        0,
        cosmetics[cID(currentTool)][cosmetics[cID(currentTool)].length - 1]
          .value.length - 1
      );
    else if (
      toolCosmetics.includes(currentTool) &&
      cosmeticTypableCharacters.includes(c.toUpperCase()) &&
      !controlling
    ) {
      if (
        cosmetics[cID(currentTool)].length &&
        cosmetics[cID(currentTool)][cosmetics[cID(currentTool)].length - 1].type
      )
        cosmetics[cID(currentTool)][
          cosmetics[cID(currentTool)].length - 1
        ].type(c);
    }
    return true;
  } else return false;
};

updateCosmeticCs = function (type, dontChange) {
  if (!dontChange)
    cosmetics[cID(currentTool)][type] = isValidHexC(
      document.getElementById(type).value
    )
      ? document.getElementById(type).value
      : "#FFFFFF";
  if (cosmetics[cID(currentTool)][type]) {
    document.getElementById(type).style["background-color"] =
      cosmetics[cID(currentTool)][type];
    document.getElementById(type).style["color"] =
      hexBrightness(cosmetics[cID(currentTool)][type]) > 0.4
        ? "#000000"
        : "#FFFFFF";
  }
};
