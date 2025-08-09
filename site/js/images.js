editIcon = new Image();
pauseIcon = new Image();
playIcon = new Image();

updateImages = function () {
  editIcon.src =
    "./img/edit" + (boolSettings["Dark Mode"] ? "_dark" : "") + ".png";
  pauseIcon.src =
    "./img/pause" + (boolSettings["Dark Mode"] ? "_dark" : "") + ".png";
  playIcon.src =
    "./img/play" + (boolSettings["Dark Mode"] ? "_dark" : "") + ".png";
};
