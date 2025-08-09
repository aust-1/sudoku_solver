categorizeTools = function () {
  boolConstraints = [
    "Diagonal +",
    "Diagonal -",
    "Antiknight",
    "Antiking",
    "Disjoint Groups",
    "Nonconsecutive",
  ];
  toolConstraints = [
    "Extra Region",
    "Odd",
    "Even",
    "Thermometer",
    /*'Slow Thermometer',*/ "Palindrome",
    "Killer Cage",
    "Little Killer Sum",
    "Sandwich Sum",
    "Difference",
    "Ratio",
    "Clone",
    "Arrow",
    "Between Line",
    "Minimum",
    "Maximum",
    "XV",
    "Quadruple",
  ];
  selectableConstraints = ["Given Digit", "Regions"];
  lineConstraints = [
    "Thermometer",
    /*'Slow Thermometer',*/ "Palindrome",
    "Arrow",
    "Between Line",
  ];
  regionConstraints = ["Extra Region", "Killer Cage", "Clone", "Arrow"];
  diagonalRegionConstraints = ["Extra Region"];
  borderConstraints = ["Difference", "Ratio", "XV"];
  cornerConstraints = ["Quadruple"];
  outsideConstraints = ["Little Killer Sum", "Sandwich Sum"];
  outsideCornerConstraints = ["Little Killer Sum"];
  typableConstraints = [
    "Killer Cage",
    "Little Killer Sum",
    "Sandwich Sum",
    "Difference",
    "Ratio",
    "Quadruple",
  ];
  perCellConstraints = ["Odd", "Even", "Minimum", "Maximum"];
  negativableConstraints = ["Ratio", "XV"];
  draggableConstraints = [
    ...new Set([...lineConstraints, ...regionConstraints]),
  ];
  multicellConstraints = [
    ...new Set([
      ...lineConstraints,
      ...regionConstraints,
      ...borderConstraints,
      ...cornerConstraints,
    ]),
  ];
  betweenCellConstraints = [...borderConstraints, ...cornerConstraints];
  allConstraints = [...boolConstraints, ...toolConstraints];

  toolCosmetics = ["Text", "Circle", "Rectangle", "Line", "Cage"];
  selectableCosmetics = [];
  lineCosmetics = ["Line"];
  regionCosmetics = ["Cage"];
  diagonalRegionCosmetics = [];
  outsideCosmetics = ["Text", "Circle", "Rectangle"];
  outsideCornerCosmetics = ["Text", "Circle", "Rectangle"];
  undraggableCosmetics = ["Text", "Circle", "Rectangle"];
  draggableCosmetics = [...new Set([...lineCosmetics, ...regionCosmetics])];
  multicellCosmetics = [
    ...new Set([...undraggableCosmetics, ...draggableCosmetics]),
  ];
  allCosmetics = toolCosmetics;

  tools = [...toolConstraints, ...toolCosmetics];
  selectableTools = [...selectableConstraints, ...selectableCosmetics];
  lineTools = [...lineConstraints, ...lineCosmetics];
  regionTools = [...regionConstraints, ...regionCosmetics];
  diagonalRegionTools = [
    ...diagonalRegionConstraints,
    ...diagonalRegionCosmetics,
  ];
  outsideTools = [...outsideConstraints, ...outsideCosmetics];
  outsideCornerTools = [...outsideCornerConstraints, ...outsideCornerCosmetics];
  oneCellAtATimeTools = [
    ...perCellConstraints,
    ...draggableConstraints,
    ...draggableCosmetics,
  ];
  draggableTools = [...draggableConstraints, ...draggableCosmetics];
  multicellTools = [...multicellConstraints, ...multicellCosmetics];
};
