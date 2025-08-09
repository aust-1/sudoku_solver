const descriptions = {
  "Given Digit": [
    "Cells with given digits must not change.",
    "",
    "Click and drag to select cells.",
    "Type to enter a number.",
  ],

  Regions: [
    "Numbers must not repeat in a region.",
    "",
    "Click and drag to select cells.",
    "Type a number to make the selection part of a certain region number.",
  ],

  "Diagonal +": ["Numbers must not repeat on the positive diagonal."],

  "Diagonal -": ["Numbers must not repeat on the negative diagonal."],

  Antiknight: [
    "Cells that are a chess knight's move",
    "apart must not contain the same number.",
  ],

  Antiking: [
    "Cells that are a chess king's move",
    "apart must not contain the same number.",
  ],

  "Disjoint Groups": [
    "Cells that appear in the same position relative to",
    "their default regions must not contain the same number.",
  ],

  Nonconsecutive: [
    "Orthogonally adjacent cells must",
    "not contain consecutive numbers.",
  ],

  "Extra Region": [
    "Numbers must not repeat in an extra region.",
    "",
    "Click and drag to draw an extra region.",
    "Click on an extra region to remove it.",
  ],

  Odd: [
    "Cells with grey circles must",
    "contain odd numbers.",
    "",
    "Click on a cell to add an odd constraint.",
    "Click on an odd constraint to remove it.",
  ],

  Even: [
    "Cells with grey squares must",
    "contain even numbers.",
    "",
    "Click on a cell to add an even constraint.",
    "Click on an even constraint to remove it.",
  ],

  Thermometer: [
    "Numbers on a thermometer must strictly",
    "increase as they move away from the bulb.",
    "",
    "Click and drag to draw a thermometer.",
    "Click on a thermometer to remove it.",
    "Shift click and drag to draw a branching thermometer.",
  ],

  Palindrome: [
    "If a number appears as the Xth cell from one",
    "end of a palindrome, it must also appear as",
    "the Xth cell from the other end.",
    "",
    "Click and drag to draw a palindrome.",
    "Click on a palindrome to remove it.",
    "Shift click and drag to draw overlapping palindromes.",
  ],

  "Killer Cage": [
    "Numbers must not repeat in a killer cage. The numbers in the",
    "cage must sum to the given total in the top left (if one exists).",
    "",
    "Click and drag to draw a cage.",
    "Click on a cage to remove it.",
    "Shift click on a cage to select it.",
    "Shift click and drag to extend an existing cage.",
    "Type to enter a total into the selected cage (or the most recently edited one).",
  ],

  "Little Killer Sum": [
    "The numbers along the indicated diagonal must sum to the given total.",
    "",
    "Click outside the grid to add a little killer sum.",
    "Click on a little killer sum to remove it.",
    "Shift click on a little killer sum to select it.",
    "Type to enter a total into the selected little killer sum (or the most recently edited one).",
  ],

  "Sandwich Sum": [
    "The numbers located between the lowest and highest numbers in the",
    "row or column relevant to the clue must sum to the indicated value.",
    "",
    "Click outside the grid to add a sandwich sum.",
    "Click on a sandwich sum to remove it.",
    "Shift click on a sandwich sum to select it.",
    "Type to enter a total into the selected sandwich sum (or the most recently edited one).",
  ],

  Difference: [
    "Numbers that appear in the cells between a difference",
    "constraint must have a difference of the indicated number.",
    "If no number is entered, the difference will be assumed to be 1.",
    "",
    "This overrides the nonconsecutive and negative ratio constraints.",
    "",
    "Click on a cell border to place a difference constraint.",
    "Click on a difference constraint to remove it.",
    "Shift click on a difference constraint to select it.",
    "Type to enter a number into the selected difference constraint (or the most recently edited one).",
  ],

  Ratio: [
    "Numbers that appear in the cells between a ratio",
    "constraint must have a ratio of the indicated number.",
    "If no number is entered, the ratio will be assumed to be 2.",
    "",
    "This overrides the nonconsecutive constraint.",
    "",
    "Click on a cell border to place a ratio constraint.",
    "Click on a ratio constraint to remove it.",
    "Shift click on a ratio constraint to select it.",
    "Type to enter a number into the selected ratio constraint (or the most recently edited one).",
  ],

  "Ratio-": [
    "Numbers that appear in cells not between a ratio",
    "constraint must not have a ratio of any ratio constraint",
    "that appears in the grid. If no ratio constraints exist,",
    "the only disallowed ratio will be 2.",
  ],

  Clone: [
    "Numbers that appear in one part of a clone must",
    "appear in exactly the same position in the other part.",
    "",
    "Click and drag to draw a clone.",
    "Click on a clone to remove it.",
    "Shift click and drag to move the secondary part of a clone.",
  ],

  Arrow: [
    "Numbers along an arrow must sum to the",
    "number shown in the circled cells.",
    "",
    "Click and drag to draw an arrow's circled sum.",
    "Shift click and drag to draw an arrow from a circled sum.",
    "Click on an arrow to remove it.",
    "Click on an arrow's circled sum to remove it.",
  ],

  "Between Line": [
    "Numbers along a between line must be between the",
    "numbers on the circled ends of the line.",
    "",
    "Click and drag to draw a between line.",
    "Click on a between line to remove it.",
  ],

  Minimum: [
    "Cells with arrows facing inward must contain numbers less",
    "than all orthogonal cells that don't also contain minimum constraints.",
    "",
    "Click on a cell to add a minimum constraint.",
    "Click on a minimum constraint to remove it.",
  ],

  Maximum: [
    "Cells with arrows facing outward must contain numbers greater",
    "than all orthogonal cells that don't also contain maximum constraints.",
    "",
    "Click on a cell to add a maximum constraint.",
    "Click on a maximum constraint to remove it.",
  ],

  XV: [
    "Cells separated by an X must sum to 10.",
    "Cells separated by a V must sum to 5.",
    "",
    "Click on a cell border to add an XV constraint.",
    "Click on an XV constraint to remove it.",
    "Shift click on an XV constraint to select it.",
    'Type "X" or "V" to enter a sum into the selected XV constraint (or the most recently edited one).',
  ],

  "XV-": ["Cells not separated by an X or a V must not sum to 10 or 5."],

  Quadruple: [
    "Each of the numbers in a quadruple constraint",
    "must appear in its four surrounding cells.",
    "",
    "Click on a cell corner to add a quadruple.",
    "Click on a quadruple to remove it.",
    "Shift click on a quadruple to select it.",
    "Type to enter numbers into the selected quadruple (or the most recently edited one).",
  ],
};
