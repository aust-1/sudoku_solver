const timer = function () {
  this.timestamps = [];
  this.paused = true;
  this.shown = true;

  this.start = function () {
    if (this.paused) {
      this.timestamps.push(new Date().getTime());
      this.paused = false;
    }
  };

  this.pause = function () {
    if (!this.paused) {
      this.timestamps.push(new Date().getTime());
      this.paused = true;
    }
  };

  this.toggle = function () {
    if (this.paused) this.start();
    else this.pause();
  };

  this.restart = function (play) {
    this.timestamps = [];
    this.paused = true;

    if (play) this.start();
  };

  this.getMS = function () {
    const timestamps = this.timestamps.concat(new Date().getTime());
    var totalMS = 0;

    for (var a = 0; a < this.timestamps.length; a++)
      totalMS += (timestamps[a + 1] - timestamps[a]) * ((a + 1) % 2);

    return totalMS;
  };

  this.getTime = function (digits) {
    if (
      digits !== undefined &&
      (isNaN(digits) || digits < 0 || digits > 3 || digits % 1 !== 0)
    ) {
      throw new Error("The digits argument must be an integer between 0 and 3");
      return;
    }

    var sec = (this.getMS() / 1000).toFixed(3);
    var min = 0;
    var hr = 0;

    if (sec >= 60) {
      min = Math.floor(sec / 60);
      sec = (sec % 60).toFixed(3);

      if (min >= 60) {
        hr = Math.floor(min / 60);
        min %= 60;

        var length = 3;
      } else var length = 2;
    } else var length = 1;

    hr = hr.toFixed(0);
    min = min.toFixed(0);

    if (sec < 10) sec = "0" + sec;
    if (min < 10) min = "0" + min;

    sec = sec.substring(0, digits ? 3 + digits : 2);

    if (length === 3) return hr + ":" + min + ":" + sec;
    if (length <= 2) return min + ":" + sec;
  };
};
