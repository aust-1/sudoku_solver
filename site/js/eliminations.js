reduceCandidatesFromUpdatesToCell = function (cell) {
  // Seen Directly

  getCellsSeenByCell(cell).forEach(
    (a) => (a.candidates = a.candidates.filter((b) => b !== cell.value))
  );
};

candidatePossibleInCell = function (n, cell, options) {
  if (n < 1 || n > size) return false;
  if (!options) options = {};
  if (!options.bruteForce && cell.value) return cell.value === n;

  // Seen Directly

  if (getCellsSeenByRow(cell, n)) return false;
  if (getCellsSeenByColumn(cell, n)) return false;
  if (getCellsSeenByRegion(cell, n)) return false;
  if (getCellsSeenByDiagonal(cell, n)) return false;
  if (getCellsSeenByKnightsMove(cell, n)) return false;
  if (getCellsSeenByKingsMove(cell, n)) return false;
  if (getCellsSeenByDisjointGroup(cell, n)) return false;
  if (getCellsSeenByExtraRegion(cell, n)) return false;
  if (getCellsSeenByKillerCage(cell, n)) return false;

  // Nonconsecutive

  if (constraints[cID("Nonconsecutive")]) {
    var cells = getCellsOrthogonalToAndIncludingCell(cell).filter(
      (a) => a !== cell
    );
    for (var a = 0; a < cells.length; a++) {
      if (
        cells[a].value &&
        Math.abs(cells[a].value - n) === 1 &&
        constraints[cID("Difference")].findIndex(
          (b) => b.cells.includes(cell) && b.cells.includes(cells[a])
        ) === -1 &&
        constraints[cID("Ratio")].findIndex(
          (b) => b.cells.includes(cell) && b.cells.includes(cells[a])
        ) === -1
      )
        return false;
    }
  }

  // Parity

  if (
    constraints[cID("Odd")].findIndex((a) => a.cell === cell) >= 0 &&
    n % 2 === 0
  )
    return false;
  if (
    constraints[cID("Even")].findIndex((a) => a.cell === cell) >= 0 &&
    n % 2 === 1
  )
    return false;

  // Thermometers

  for (var a = 0; a < constraints[cID("Thermometer")].length; a++) {
    const currentThermometer = constraints[cID("Thermometer")][a];
    for (var b = 0; b < currentThermometer.lines.length; b++) {
      const index = currentThermometer.lines[b].indexOf(cell);
      if (index > -1) {
        if (n < index + 1) return false;
        if (n > size - (currentThermometer.lines[b].length - (index + 1)))
          return false;

        var compareIndex = index + 1;
        while (compareIndex < currentThermometer.lines[b].length) {
          if (
            (currentThermometer.lines[b][compareIndex].value &&
              currentThermometer.lines[b][compareIndex].value <= n) ||
            (!currentThermometer.lines[b][compareIndex].value &&
              currentThermometer.lines[b][compareIndex].candidates.every(
                (c) => c <= n
              ))
          )
            return false;
          compareIndex++;
        }

        var compareIndex = index - 1;
        while (compareIndex >= 0) {
          if (
            (currentThermometer.lines[b][compareIndex].value &&
              currentThermometer.lines[b][compareIndex].value >= n) ||
            (!currentThermometer.lines[b][compareIndex].value &&
              currentThermometer.lines[b][compareIndex].candidates.every(
                (c) => c >= n
              ))
          )
            return false;
          compareIndex--;
        }
      }
    }
  }

  // Slow Thermometers
  /*
	const seen = getCellsSeenByCell(cell);
	for(var a = 0; a < constraints[cID('Slow Thermometer')].length; a++){
		const currentThermometer = constraints[cID('Slow Thermometer')][a];
		for(var b = 0; b < currentThermometer.lines.length; b++){
			const index = currentThermometer.lines[b].indexOf(cell);
			if(index > -1){
				var compareIndex = index + 1;
				while(compareIndex < currentThermometer.lines[b].length){
					if(seen.includes(currentThermometer.lines[b][compareIndex])){
						if(( currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].value <= n) ||
						   (!currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].candidates.every(c => c <= n)))
							return false;
					} else {
						if(( currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].value < n) ||
						   (!currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].candidates.every(c => c < n)))
							return false;
					}
					compareIndex++;
				}

				var compareIndex = index - 1;
				while(compareIndex >= 0){
					if(seen.includes(currentThermometer.lines[b][compareIndex])){
						if(( currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].value >= n) ||
						   (!currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].candidates.every(c => c >= n)))
							return false;
					} else {
						if(( currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].value > n) ||
						   (!currentThermometer.lines[b][compareIndex].value && currentThermometer.lines[b][compareIndex].candidates.every(c => c > n)))
							return false;
					}
					compareIndex--;
				}
			}
		}
	}
	*/

  // Palindromes

  if (!options.stopLoops) {
    for (var a = 0; a < constraints[cID("Palindrome")].length; a++) {
      const currentPalindrome = constraints[cID("Palindrome")][a];
      for (var b = 0; b < currentPalindrome.lines.length; b++) {
        const index = currentPalindrome.lines[b].indexOf(cell);
        if (index > -1) {
          const currentCell = currentPalindrome.lines[b][index];
          const oppositeCell =
            currentPalindrome.lines[b][
              currentPalindrome.lines[b].length - index - 1
            ];
          if (oppositeCell.value && oppositeCell.value !== n) return false;
          else if (
            !candidatePossibleInCell(n, oppositeCell, { stopLoops: true })
          )
            return false;
        }
      }
    }
  }

  // Killer Cages

  for (var a = 0; a < constraints[cID("Killer Cage")].length; a++) {
    const currentCage = constraints[cID("Killer Cage")][a];
    const index = currentCage.cells.indexOf(cell);
    if (index > -1) {
      var sum = n;
      var emptyCells = 0;
      for (var b = 0; b < currentCage.cells.length; b++) {
        if (currentCage.cells[b] !== cell) {
          sum += currentCage.cells[b].value;
          if (!currentCage.cells[b].value) emptyCells++;
        }
      }

      if (currentCage.value.length) {
        if (sum > parseInt(currentCage.value) - minInNCells(emptyCells))
          return false;
        if (sum < parseInt(currentCage.value) - maxInNCells(emptyCells))
          return false;
      }
    }
  }

  // Little Killer Sums

  for (var a = 0; a < constraints[cID("Little Killer Sum")].length; a++) {
    const currentLKSum = constraints[cID("Little Killer Sum")][a];
    if (currentLKSum.value.length) {
      var index = currentLKSum.cells.indexOf(cell);
      if (index > -1) {
        if (
          currentLKSum.minSum(index) + n > currentLKSum.value ||
          currentLKSum.maxSum(index) + n < currentLKSum.value
        )
          return false;
      }
    }
  }

  // Sandwich Sums

  for (var a = 0; a < constraints[cID("Sandwich Sum")].length; a++) {
    const currentSandwich = constraints[cID("Sandwich Sum")][a];
    if (currentSandwich.value.length) {
      const index = currentSandwich.set.indexOf(cell);
      if (index > -1) {
        const minDistance = Math.min(
          ...currentSandwich.sums.map((b) => b.length)
        );
        const maxDistance = Math.max(
          ...currentSandwich.sums.map((b) => b.length)
        );
        if (
          [1, size].includes(n) &&
          index < minDistance + 1 &&
          index > size - (minDistance + 1) - 1
        )
          return false;

        const values = currentSandwich.set.map((b) => b.value);
        values[index] = n;

        const ends = currentSandwich.getEnds();
        if ([1, size].includes(n)) ends.push(index);
        const end1 = Math.min(...ends);
        const end2 = Math.max(...ends);

        if (end1 >= 0 && end2 >= 0 && end1 !== end2) {
          const distance = Math.abs(end1 - end2) - 1;
          if (
            [1, size].includes(n) &&
            (distance < minDistance || distance > maxDistance)
          )
            return false;

          var sum = 0;
          var emptyCells = 0;
          for (var b = end1 + 1; b < end2; b++) {
            sum += values[b];
            if (!values[b]) emptyCells++;
          }

          if (
            sum >
            parseInt(currentSandwich.value) -
              (minInNCells(emptyCells) + emptyCells)
          )
            return false;
          if (
            sum <
            parseInt(currentSandwich.value) -
              (maxInNCells(emptyCells) - emptyCells)
          )
            return false;
        }
      }
    }
  }

  // Differences

  for (var a = 0; a < constraints[cID("Difference")].length; a++) {
    const currentDifference = constraints[cID("Difference")][a];
    const index = currentDifference.cells.indexOf(cell);
    if (index > -1) {
      const oppositeIndex = (index + 1) % 2;
      if (
        currentDifference.cells[oppositeIndex].value &&
        Math.abs(currentDifference.cells[oppositeIndex].value - n) !==
          parseInt(currentDifference.value || 1)
      )
        return false;
    }
  }

  // Ratios

  for (var a = 0; a < constraints[cID("Ratio")].length; a++) {
    const currentRatio = constraints[cID("Ratio")][a];
    const index = currentRatio.cells.indexOf(cell);
    if (index > -1) {
      const oppositeIndex = (index + 1) % 2;
      if (
        currentRatio.cells[oppositeIndex].value &&
        Math.max(
          currentRatio.cells[oppositeIndex].value / n,
          n / currentRatio.cells[oppositeIndex].value
        ) !== parseInt(currentRatio.value || 2)
      )
        return false;
    }
  }

  if (constraints[cID("Ratio")].negative) {
    const affected = getCellsOrthogonalToAndIncludingCell(cell).filter(
      (a) =>
        a !== cell &&
        constraints[cID("Ratio")].every(
          (b) => !b.cells.includes(cell) || !b.cells.includes(a)
        )
    );
    const disallowedRatios = [
      ...new Set(constraints[cID("Ratio")].map((b) => parseInt(b.value) || 2)),
    ];
    if (!constraints[cID("Ratio")].length && !disallowedRatios.includes(2))
      disallowedRatios.push(2);
    for (var a = 0; a < affected.length; a++) {
      if (
        affected[a].value &&
        (disallowedRatios.includes(affected[a].value / n) ||
          disallowedRatios.includes(n / affected[a].value)) &&
        constraints[cID("Difference")].findIndex(
          (b) => b.cells.includes(cell) && b.cells.includes(affected[a])
        ) === -1
      )
        return false;
    }
  }

  // Clones

  if (!options.stopLoops) {
    for (var a = 0; a < constraints[cID("Clone")].length; a++) {
      const currentClone = constraints[cID("Clone")][a];
      const index = Math.max(
        currentClone.cells.indexOf(cell),
        currentClone.cloneCells.indexOf(cell)
      );
      if (index > -1) {
        const cell1 = currentClone.cells[index];
        const cell2 = currentClone.cloneCells[index];
        if (
          (cell1.value && cell1.value !== n) ||
          (cell2.value && cell2.value !== n)
        )
          return false;
        else if (
          !candidatePossibleInCell(n, cell1, { stopLoops: true }) ||
          !candidatePossibleInCell(n, cell2, { stopLoops: true })
        )
          return false;
      }
    }
  }

  // Arrows

  for (var a = 0; a < constraints[cID("Arrow")].length; a++) {
    const currentArrow = constraints[cID("Arrow")][a];
    var index = currentArrow.cells.indexOf(cell);
    if (index > -1) {
      if (
        currentArrow.lines.some(
          (b) =>
            currentArrow.minSum(currentArrow.lines.indexOf(b)) >
            currentArrow.maxValue(n, index)
        ) ||
        currentArrow.lines.some(
          (b) =>
            currentArrow.maxSum(currentArrow.lines.indexOf(b)) <
            currentArrow.minValue(n, index)
        )
      )
        return false;
    } else {
      for (var b = 0; b < currentArrow.lines.length; b++) {
        index = currentArrow.lines[b].indexOf(cell);
        if (index > 0) {
          if (
            currentArrow.minSum(b, index) + n > currentArrow.maxValue() ||
            currentArrow.maxSum(b, index) + n < currentArrow.minValue()
          )
            return false;
        }
      }
    }
  }

  // Between Lines

  for (var a = 0; a < constraints[cID("Between Line")].length; a++) {
    const currentBetweenLine = constraints[cID("Between Line")][a].lines[0];
    const index = currentBetweenLine.indexOf(cell);
    if (index > -1) {
      if (index > 0 && index < currentBetweenLine.length - 1) {
        if (
          !(
            n >
              (currentBetweenLine[0].value ||
                Math.min(...currentBetweenLine[0].candidates)) &&
            n <
              (currentBetweenLine[currentBetweenLine.length - 1].value ||
                Math.max(
                  ...currentBetweenLine[currentBetweenLine.length - 1]
                    .candidates
                ))
          ) &&
          !(
            n <
              (currentBetweenLine[0].value ||
                Math.max(...currentBetweenLine[0].candidates)) &&
            n >
              (currentBetweenLine[currentBetweenLine.length - 1].value ||
                Math.min(
                  ...currentBetweenLine[currentBetweenLine.length - 1]
                    .candidates
                ))
          )
        )
          return false;
      } else {
        const oppositeCell =
          currentBetweenLine[
            (index + (currentBetweenLine.length - 1)) %
              (2 * (currentBetweenLine.length - 1))
          ];
        if (oppositeCell) {
          if (
            !(
              currentBetweenLine
                .slice(1, currentBetweenLine.length - 1)
                .every((b) => Math.min(...b.candidates) < n) ||
              currentBetweenLine
                .slice(1, currentBetweenLine.length - 1)
                .every((b) => Math.max(...b.candidates) > n)
            )
          )
            return false;
          if (oppositeCell.value) {
            for (var b = 1; b < currentBetweenLine.length - 1; b++) {
              if (currentBetweenLine[b].value) {
                if (
                  Math.sign(
                    oppositeCell.value - currentBetweenLine[b].value
                  ) !== Math.sign(currentBetweenLine[b].value - n)
                )
                  return false;
              }
            }
          }
        }
      }
    }
  }

  // Extremes

  if (constraints[cID("Minimum")].findIndex((a) => a.cell === cell) >= 0) {
    if (
      getCellsOrthogonalToAndIncludingCell(cell).some(
        (a) =>
          constraints[cID("Minimum")].findIndex((b) => b.cell === a) === -1 &&
          a.value &&
          a.value <= n
      )
    )
      return false;
  } else {
    if (
      getCellsOrthogonalToAndIncludingCell(cell).some(
        (a) =>
          constraints[cID("Minimum")].findIndex((b) => b.cell === a) >= 0 &&
          (a.value ? a.value >= n : a.candidates[0] >= n)
      )
    )
      return false;
  }

  if (constraints[cID("Maximum")].findIndex((a) => a.cell === cell) >= 0) {
    if (
      getCellsOrthogonalToAndIncludingCell(cell).some(
        (a) =>
          constraints[cID("Maximum")].findIndex((b) => b.cell === a) === -1 &&
          a.value &&
          a.value >= n
      )
    )
      return false;
  } else {
    if (
      getCellsOrthogonalToAndIncludingCell(cell).some(
        (a) =>
          constraints[cID("Maximum")].findIndex((b) => b.cell === a) >= 0 &&
          (a.value ? a.value <= n : a.candidates[a.candidates.length - 1] <= n)
      )
    )
      return false;
  }

  // Xs and Vs

  for (var a = 0; a < constraints[cID("XV")].length; a++) {
    const currentXV = constraints[cID("XV")][a];
    if (currentXV.value.length) {
      const index = currentXV.cells.indexOf(cell);
      if (index > -1) {
        const oppositeIndex = (index + 1) % 2;
        if (
          currentXV.cells[oppositeIndex].value &&
          Math.abs(currentXV.cells[oppositeIndex].value + n) !==
            parseInt(currentXV.value === "X" ? 10 : 5)
        )
          return false;
      }
    }
  }

  if (constraints[cID("XV")].negative) {
    const affected = getCellsOrthogonalToAndIncludingCell(cell).filter(
      (a) =>
        a !== cell &&
        constraints[cID("XV")].every(
          (b) => !b.cells.includes(cell) || !b.cells.includes(a)
        )
    );
    for (var a = 0; a < affected.length; a++) {
      if (
        affected[a].value &&
        (affected[a].value + n === 10 || affected[a].value + n === 5)
      )
        return false;
    }
  }

  // Quadruples

  for (var a = 0; a < constraints[cID("Quadruple")].length; a++) {
    const currentQuadruple = constraints[cID("Quadruple")][a];
    if (currentQuadruple.cells.includes(cell)) {
      const used = currentQuadruple.cells
        .filter((b) => (b === cell ? n : b.value))
        .map((b) => (b === cell ? n : b.value));
      const leftToPlace = currentQuadruple.values.filter(
        (b) => !used.includes(b)
      );
      if (leftToPlace.length > 4 - used.length) return false;
    }
  }

  return true;
};
