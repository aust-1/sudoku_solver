clearConsole = function () {
  output = "";
  consoleOutput.value = "";
};

removeLastLog = function () {
  if (output.indexOf("\n") > -1)
    output = output.slice(0, output.lastIndexOf("\n"));
  else output = "";
};

log = function (text, options) {
  if (!options) options = {};

  if (options.newLine !== false) {
    if (output.length) output += "\n";
    output += "  ";
  }

  output += text;

  updateConsole();
};

updateConsole = function () {
  consoleOutput.value = output;
  consoleOutput.scrollTop = consoleOutput.scrollHeight;
};
