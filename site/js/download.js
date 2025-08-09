download = function (screenshot, customFileName) {
  togglePreview(screenshot);

  ctx = canvas2.getContext("2d");
  canvas2.width = canvas.width;
  canvas2.height = canvas.height;
  ctx.textAlign = "center";

  ctx.fillStyle = "#FFFFFF";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  drawGrid();

  ctx = canvas3.getContext("2d");
  canvas3.width = (gridSL + lineWW) * downloadResolution;
  canvas3.height = (gridSL + lineWW) * downloadResolution;
  ctx.save();
  ctx.scale(downloadResolution, downloadResolution);
  ctx.drawImage(
    canvas2,
    gridX - lineWW / 2,
    gridY - lineWW / 2,
    gridSL + lineWW,
    gridSL + lineWW,
    0,
    0,
    canvas3.width / downloadResolution,
    canvas3.height / downloadResolution
  );
  ctx.restore();

  ctx = canvas.getContext("2d");

  const link = document.createElement("a");
  link.download = (customFileName || getPuzzleTitle()) + ".png";
  link.href = canvas3.toDataURL();
  link.click();

  togglePreview(screenshot);
};
