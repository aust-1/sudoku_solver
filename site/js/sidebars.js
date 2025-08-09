sidebar = function (x, modes) {
  this.x = x;
  this.y = gridY;

  this.modes = modes;

  this.sections = [];
  this.buttons = [];

  this.show = function () {
    if (this.modes.includes(mode)) {
      ctx.lineWidth = lineWW;
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#404040" : "#D0D0D0";
      ctx.strokeStyle = boolSettings["Dark Mode"] ? "#202020" : "#808080";
      ctx.fillRect(this.x - sidebarW / 2, gridY, sidebarW, gridSL);
      ctx.strokeRect(this.x - sidebarW / 2, gridY, sidebarW, gridSL);

      for (var a = 0; a < this.sections.length; a++) this.sections[a].show();
      for (var a = 0; a < this.buttons.length; a++) this.buttons[a].show();
    }
  };

  this.showTooltip = function () {
    for (var a = 0; a < this.buttons.length; a++) this.buttons[a].showTooltip();
  };
};

createSidebars = function () {
  sidebars = [];

  createSidebarConstraints();
  createSidebarTimer();
  createSidebarMain();
  createSidebarConsole();
};

createSidebarConstraints = function () {
  var x = gridX - (sidebarDist + sidebarW / 2);
  var y = gridY;

  const sb = new sidebar(x, ["Setting"]);
  sidebars.push(sb);
  sidebars[sidebars.length - 1].title = "Constraints";

  y += buttonMargin;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Setting"], "Info", "Info")
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Setting"], "Settings", "Settings")
  );

  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y));

  y += buttonMargin;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Setting"], "New", "New Grid")
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Setting"], "Export", "Export")
  );

  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y, "Constraints"));

  y += sidebarTitleHeight + buttonMargin;
  for (var a = 0; a < boolConstraints.length; a++) {
    sb.buttons.push(
      new button(
        x - (buttonSH + buttonGap) / 2,
        y,
        buttonW - (buttonSH + buttonGap),
        buttonSH,
        ["Setting"],
        boolConstraints[a],
        boolConstraints[a]
      )
    );
    if (a < boolConstraints.length - 1) y += buttonSH + buttonGap;
  }

  y += buttonSH + buttonMargin;
  sb.sections.push(new section(x, y));

  y += buttonMargin - buttonSH - buttonGap;
  for (var a = 0; a < selectableConstraints.length; a++) {
    y += buttonSH + buttonGap;
    sb.buttons.push(
      new button(
        x,
        y,
        buttonW,
        buttonSH,
        ["Setting"],
        selectableConstraints[a],
        selectableConstraints[a]
      )
    );
  }

  y += buttonSH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonSH,
      ["Setting"],
      "ConstraintTools",
      "Constraint Tools",
      true,
      true
    )
  );
  y += buttonSH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonSH,
      ["Setting"],
      "CosmeticTools",
      "Cosmetic Tools",
      true,
      true
    )
  );

  for (var a = 0; a < toolConstraints.length; a++) {
    const currentY =
      gridY +
      gridSL -
      (buttonSH * toolConstraints.length +
        buttonGap * (toolConstraints.length - 1) +
        buttonMargin) +
      (buttonSH + buttonGap) * a;
    sb.buttons.push(
      new button(
        x + sidebarW,
        currentY,
        buttonW,
        buttonSH,
        ["Constraint Tools"],
        toolConstraints[a],
        toolConstraints[a]
      )
    );
    if (negativableConstraints.includes(toolConstraints[a]))
      sb.buttons.push(
        new button(
          x + sidebarW + buttonW / 2 + buttonGap + buttonSH / 2,
          currentY,
          buttonSH,
          buttonSH,
          ["Constraint Tools"],
          toolConstraints[a] + "-",
          "-"
        )
      );
  }

  for (var a = 0; a < toolCosmetics.length; a++) {
    const currentY =
      gridY +
      gridSL -
      (buttonSH * toolCosmetics.length +
        buttonGap * (toolCosmetics.length - 1) +
        buttonMargin) +
      (buttonSH + buttonGap) * a;
    sb.buttons.push(
      new button(
        x + sidebarW,
        currentY,
        buttonW,
        buttonSH,
        ["Cosmetic Tools"],
        toolCosmetics[a],
        toolCosmetics[a]
      )
    );
  }

  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5,
      0,
      270,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticPlaceMode",
      ""
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 - 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticSizeL",
      "<"
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 + 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticSizeR",
      ">"
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 - 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticWL",
      "<"
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 + 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticWR",
      ">"
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 - 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticHL",
      "<"
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 + 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticHR",
      ">"
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 - 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticAngleL",
      "<"
    )
  );
  sb.buttons.push(
    new button(
      gridX - sidebarDist + sidebarW * 1.5 + 110,
      0,
      50,
      buttonSH,
      ["Cosmetic Tools"],
      "CosmeticAngleR",
      ">"
    )
  );
};

createSidebarTimer = function () {
  var x = gridX - (sidebarDist + sidebarW / 2);
  var y = gridY;

  const sb = new sidebar(x, ["Solving"]);
  sidebars.push(sb);
  sidebars[sidebars.length - 1].title = "Timer";

  y += buttonMargin;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Solving"], "Info", "Info")
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Solving"], "Settings", "Settings")
  );

  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y, "Timer"));

  y += sidebarTitleHeight + buttonMargin + buttonLH + buttonMargin;
  sb.sections.push(new section(x, y));

  y += buttonMargin;
  sb.buttons.push(
    new button(
      x - ((buttonW - buttonGap * 2) / 3 + buttonGap),
      y,
      (buttonW - buttonGap * 2) / 3,
      buttonSH,
      ["Solving"],
      "HideTimer",
      ""
    )
  );
  sb.buttons.push(
    new button(
      x,
      y,
      (buttonW - buttonGap * 2) / 3,
      buttonSH,
      ["Solving"],
      "PauseTimer",
      ""
    )
  );
  sb.buttons.push(
    new button(
      x + ((buttonW - buttonGap * 2) / 3 + buttonGap),
      y,
      (buttonW - buttonGap * 2) / 3,
      buttonSH,
      ["Solving"],
      "ClearTimer",
      ""
    )
  );

  y += buttonSH + buttonMargin;
  sb.sections.push(new section(x, y));

  y += buttonMargin;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Solving"], "Screenshot", "Screenshot")
  );
  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y, customRuleset.length ? "Rules" : null));
};

createSidebarMain = function () {
  var x = gridX + gridSL + (sidebarDist + sidebarW / 2);
  var y = gridY;

  const sb = new sidebar(x, ["Setting", "Solving"]);
  sidebars.push(sb);
  sidebars[sidebars.length - 1].title = "Main";

  y += buttonMargin;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Setting", "Solving"], "Mode", "")
  );

  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y));

  y += buttonMargin;
  sb.buttons.push(
    new button(
      x - (buttonLH + buttonGap) / 2,
      y,
      buttonW - (buttonLH + buttonGap),
      buttonLH,
      ["Setting", "Solving"],
      "Solve",
      "Solve"
    )
  );
  sb.buttons.push(
    new button(
      x + buttonW / 2 - buttonLH / 2,
      y,
      buttonLH,
      buttonLH,
      ["Setting", "Solving"],
      "Camera",
      ""
    )
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(x, y, buttonW, buttonLH, ["Setting", "Solving"], "Clear", "")
  );

  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y));

  y += buttonMargin;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Setting", "Solving"],
      "EnterNormal",
      "Normal"
    )
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Setting", "Solving"],
      "EnterCorner",
      "Corner"
    )
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Setting", "Solving"],
      "EnterCenter",
      "Center"
    )
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Setting", "Solving"],
      "EnterHighlight",
      "Highlight"
    )
  );

  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y));

  y += buttonMargin;

  if (tempEnterMode === "Highlight")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  else if (selectableConstraints.includes(currentTool)) numbers = [...digits];
  else numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0];

  if (
    tempEnterMode === "Highlight" ||
    !selectableConstraints.includes(currentTool)
  )
    buttonsWide = 3;
  else if (regionW > 6)
    buttonsWide = Math.min(Math.ceil(Math.sqrt(numbers.length)), 6);
  else buttonsWide = regionW;

  const numButtonW = (buttonW - buttonGap * (buttonsWide - 1)) / buttonsWide;
  const usedButtonH = numbers.length / buttonsWide > 3 ? buttonSH : buttonLH;
  for (var i = 0; i < numbers.length / buttonsWide; i++) {
    for (var j = 0; j < buttonsWide; j++) {
      if (i * buttonsWide + j + 1 <= numbers.length)
        sb.buttons.push(
          new button(
            x - buttonW / 2 + j * (numButtonW + buttonGap) + numButtonW / 2,
            y,
            numButtonW,
            usedButtonH,
            ["Setting", "Solving"],
            String(numbers[i * buttonsWide + j]),
            ""
          )
        );
    }

    y += usedButtonH + buttonGap;
  }

  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Setting", "Solving"],
      "Delete",
      "Delete"
    )
  );

  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(
      x - (buttonW + buttonGap) / 4,
      y,
      (buttonW - buttonGap) / 2,
      buttonLH,
      ["Setting", "Solving"],
      "Undo",
      "Undo"
    )
  );
  sb.buttons.push(
    new button(
      x + (buttonW + buttonGap) / 4,
      y,
      (buttonW - buttonGap) / 2,
      buttonLH,
      ["Setting", "Solving"],
      "Redo",
      "Redo"
    )
  );
};

createSidebarConsole = function () {
  var x =
    gridX + gridSL + (sidebarDist + sidebarW) + (sidebarGap + sidebarW / 2);
  var y = gridY;

  const sb = new sidebar(x, ["Setting", "Solving"]);
  sidebars.push(sb);
  sidebars[sidebars.length - 1].title = "Console";

  y += buttonMargin;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Solving", "Setting"],
      "SolvePath",
      "Solution Path"
    )
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Solving", "Setting"],
      "SolveStep",
      "Step"
    )
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Solving", "Setting"],
      "CheckUnique",
      "Check"
    )
  );
  y += buttonLH + buttonGap;
  sb.buttons.push(
    new button(
      x,
      y,
      buttonW,
      buttonLH,
      ["Solving", "Setting"],
      "CountSolutions",
      "Solution Count"
    )
  );

  y += buttonLH + buttonMargin;
  sb.sections.push(new section(x, y));
};
