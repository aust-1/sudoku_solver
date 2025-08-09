setPuzzleInfo = function () {
  customTitle = document.getElementById("title").value.trim();
  author = document.getElementById("author").value.trim();
  customRuleset = document.getElementById("ruleset").value;

  closePopups();
};

getPuzzleTitle = function () {
  var title = "";

  ctx.font = titleLSize + "px Arial";

  if (customTitle.length) title = customTitle;
  else {
    if (size !== 9) title += size + "x" + size + " ";
    if (
      getCells().some(
        (a) =>
          a.region !==
          Math.floor(a.i / regionH) * regionH + Math.floor(a.j / regionW)
      )
    )
      title += "Irregular ";
    if (constraints[cID("Extra Region")].length) title += "Extra-Region ";
    if (constraints[cID("Odd")].length && !constraints[cID("Even")].length)
      title += "Odd ";
    if (!constraints[cID("Odd")].length && constraints[cID("Even")].length)
      title += "Even ";
    if (constraints[cID("Odd")].length && constraints[cID("Even")].length)
      title += "Odd-Even ";
    if (constraints[cID("Diagonal +")] !== constraints[cID("Diagonal -")])
      title += "Single-Diagonal ";
    if (
      constraints[cID("Nonconsecutive")] &&
      !(
        constraints[cID("Difference")].length &&
        constraints[cID("Difference")].some((a) => ["", "1"].includes(a.value))
      ) &&
      !constraints[cID("Ratio")].negative
    )
      title += "Nonconsecutive ";
    if (
      constraints[cID("Nonconsecutive")] &&
      constraints[cID("Difference")].length &&
      constraints[cID("Difference")].some((a) => ["", "1"].includes(a.value)) &&
      !constraints[cID("Ratio")].negative
    )
      title += "Consecutive ";
    if (
      !constraints[cID("Nonconsecutive")] &&
      constraints[cID("Difference")].length &&
      constraints[cID("Difference")].every((a) => ["", "1"].includes(a.value))
    )
      title += "Consecutive-Pairs ";
    if (constraints[cID("Antiknight")]) title += "Antiknight ";
    if (constraints[cID("Antiking")]) title += "Antiking ";
    if (constraints[cID("Disjoint Groups")]) title += "Disjoint-Group ";
    if (constraints[cID("XV")].length || constraints[cID("XV")].negative)
      title += "XV " + (constraints[cID("XV")].negative ? "(-) " : "");
    if (constraints[cID("Little Killer Sum")].length) title += "Little Killer ";
    if (constraints[cID("Sandwich Sum")].length) title += "Sandwich ";
    if (constraints[cID("Thermometer")].length) title += "Thermo ";
    if (constraints[cID("Palindrome")].length) title += "Palindrome ";
    if (
      constraints[cID("Difference")].length &&
      constraints[cID("Difference")].some(
        (a) => !["", "1"].includes(a.value)
      ) &&
      !(
        constraints[cID("Nonconsecutive")] && constraints[cID("Ratio")].negative
      )
    )
      title += "Difference ";
    if (
      (constraints[cID("Ratio")].length ||
        constraints[cID("Ratio")].negative) &&
      !(
        constraints[cID("Nonconsecutive")] && constraints[cID("Ratio")].negative
      )
    )
      title += "Ratio " + (constraints[cID("Ratio")].negative ? "(-) " : "");
    if (
      constraints[cID("Nonconsecutive")] &&
      constraints[cID("Ratio")].negative
    )
      title += "Kropki ";
    if (constraints[cID("Killer Cage")].length) title += "Killer ";
    if (constraints[cID("Clone")].length) title += "Clone ";
    if (constraints[cID("Arrow")].length) title += "Arrow ";
    if (constraints[cID("Between Line")].length) title += "Between ";
    if (constraints[cID("Quadruple")].length) title += "Quadruples ";
    if (
      constraints[cID("Minimum")].length ||
      constraints[cID("Maximum")].length
    )
      title += "Extremes ";

    title += "Sudoku";

    if (constraints[cID("Diagonal +")] && constraints[cID("Diagonal -")])
      title += " X";

    if (title === "Sudoku") title = "Classic Sudoku";

    if (ctx.measureText(title).width > canvas.width * maxTitleW)
      title = "Extreme Variant Sudoku";
  }

  buttons[buttons.findIndex((a) => a.id === "EditInfo")].x =
    canvas.width / 2 + ctx.measureText(title).width / 2 + 40;

  return title;
};
