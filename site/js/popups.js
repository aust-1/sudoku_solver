const buttons = [];

createOtherButtons = function () {
  buttons.push(
    new button(
      canvas.width / 2 + popups[cID("Info")].w / 2,
      canvas.height / 2 - popups[cID("Info")].h / 2 - 20,
      40,
      40,
      ["Info"],
      "X",
      "X"
    )
  );

  buttons.push(
    new button(
      canvas.width / 2 + popups[cID("Settings")].w / 2,
      canvas.height / 2 - popups[cID("Settings")].h / 2 - 20,
      40,
      40,
      ["Settings"],
      "X",
      "X"
    )
  );
  for (var a = 0; a < boolSettings.length - 1; a++)
    buttons.push(
      new button(
        canvas.width / 2 - (buttonSH + buttonGap) / 2,
        canvas.height / 2 -
          popups[cID("Settings")].h / 2 +
          110 +
          (buttonSH + buttonGap) * a,
        450,
        buttonSH,
        ["Settings"],
        boolSettings[a],
        boolSettings[a]
      )
    );
  buttons.push(
    new button(
      canvas.width / 2 - (buttonSH + buttonGap) / 2,
      canvas.height / 2 + popups[cID("Settings")].h / 2 - 50,
      450,
      buttonSH,
      ["Settings"],
      boolSettings[boolSettings.length - 1],
      boolSettings[boolSettings.length - 1]
    )
  );

  buttons.push(
    new button(
      canvas.width / 2 + popups[cID("New Grid")].w / 2,
      canvas.height / 2 - popups[cID("New Grid")].h / 2 - 20,
      40,
      40,
      ["New Grid"],
      "X",
      "X"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2 - popups[cID("New Grid")].w * 0.222,
      canvas.height / 2 - popups[cID("New Grid")].h * 0.055,
      60,
      50,
      ["New Grid"],
      "Size-",
      "<"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2 + popups[cID("New Grid")].w * 0.222,
      canvas.height / 2 - popups[cID("New Grid")].h * 0.055,
      60,
      50,
      ["New Grid"],
      "Size+",
      ">"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2,
      canvas.height / 2 + popups[cID("New Grid")].h * 0.222,
      275,
      buttonLH,
      ["New Grid"],
      "ConfirmNew",
      "Confirm"
    )
  );

  buttons.push(
    new button(
      canvas.width / 2 + popups[cID("Export")].w / 2,
      canvas.height / 2 - popups[cID("Export")].h / 2 - 20,
      40,
      40,
      ["Export"],
      "X",
      "X"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2 - 175 - (buttonSH + buttonGap) / 2,
      canvas.height / 2 - 45,
      390 - (buttonSH + buttonGap),
      buttonSH,
      ["Export"],
      "DisableHC",
      "Disable Conflict Highlighting"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2 - 175,
      canvas.height / 2 + 6 + (buttonLH + buttonGap) * 0,
      400,
      buttonLH,
      ["Export"],
      "Download",
      "Download Image"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2 - 175,
      canvas.height / 2 + 6 + (buttonLH + buttonGap) * 1,
      400,
      buttonLH,
      ["Export"],
      "Screenshot",
      "Download Screenshot"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2 - 175,
      canvas.height / 2 + 6 + (buttonLH + buttonGap) * 2,
      400,
      buttonLH,
      ["Export"],
      "OpenLink",
      "Open With Link"
    )
  );

  buttons.push(
    new button(0, 45, 22, 22, ["Setting"], "EditInfo", "Edit Info", false)
  );
  buttons.push(
    new button(
      canvas.width / 2 + popups[cID("Edit Info")].w / 2,
      canvas.height / 2 - popups[cID("Edit Info")].h / 2 - 20,
      40,
      40,
      ["Edit Info"],
      "X",
      "X"
    )
  );
  buttons.push(
    new button(
      canvas.width / 2,
      canvas.height / 2 + 240,
      275,
      buttonLH,
      ["Edit Info"],
      "ConfirmInfo",
      "Confirm"
    )
  );
};

togglePopup = function (title) {
  closePopups();
  popup = title;

  setCameraX(0);

  if (title === "Settings") {
    document.getElementById("bruteForceTimeLimit").style.display = "block";
    document.getElementById("solutionCountLimit").style.display = "block";
    document.getElementById("minStepDelay").style.display = "block";
  } else if (title === "Export") {
    document.getElementById("previewTypeBox").style.display = "block";
  } else if (title === "Edit Info") {
    document.getElementById("title").style.display = "block";
    document.getElementById("author").style.display = "block";
    document.getElementById("ruleset").style.display = "block";
    document.getElementById("title").value = customTitle;
    document.getElementById("author").value = author;
    document.getElementById("ruleset").value = customRuleset;
    setTimeout(function () {
      document.getElementById("title").focus();
    }, 1);
  }
};

closePopups = function () {
  popup = null;
  document.activeElement = document;

  document.getElementById("bruteForceTimeLimit").style.display = "none";
  document.getElementById("solutionCountLimit").style.display = "none";
  document.getElementById("minStepDelay").style.display = "none";
  document.getElementById("previewTypeBox").style.display = "none";
  document.getElementById("baseC").style.display = "none";
  document.getElementById("outlineC").style.display = "none";
  document.getElementById("fontC").style.display = "none";
  document.getElementById("colorPicker").style.display = "none";
  document.getElementById("title").style.display = "none";
  document.getElementById("author").style.display = "none";
  document.getElementById("ruleset").style.display = "none";
};

createCosmeticPopup = function (sampleObj) {
  cosmeticEditMenuH =
    buttonMargin * 2 +
    (undraggableCosmetics.includes(currentTool)
      ? buttonSH + buttonGap + 15
      : 0) +
    (sampleObj.size !== undefined ? buttonSH + buttonGap : 0) +
    (sampleObj.width !== undefined ? buttonSH + buttonGap : 0) +
    (sampleObj.height !== undefined ? buttonSH + buttonGap : 0) +
    (sampleObj.angle !== undefined ? buttonSH + buttonGap : 0) +
    (sampleObj.baseC ? buttonSH + cosmeticEditMenuCBoxGap : 0) +
    (sampleObj.outlineC ? buttonSH + cosmeticEditMenuCBoxGap : 0) +
    (sampleObj.fontC ? buttonSH + cosmeticEditMenuCBoxGap : 0) -
    buttonGap;
  cosmeticEditMenuY = Math.min(
    gridY + gridSL - cosmeticEditMenuH,
    Math.max(
      mouseY - cosmeticEditMenuYOffset,
      gridY +
        gridSL -
        (buttonSH * toolCosmetics.length +
          buttonGap * (toolCosmetics.length - 1) +
          buttonMargin * 2)
    )
  );
};
