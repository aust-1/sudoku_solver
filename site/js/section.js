section = function (x, y, title) {
  this.x = x;
  this.y = y;

  this.h = title ? sidebarTitleHeight : 0;

  this.title = title;

  this.show = function () {
    ctx.lineWidth = lineWW;
    ctx.fillStyle = boolSettings["Dark Mode"] ? "#303030" : "#C0C0C0";
    ctx.strokeStyle = boolSettings["Dark Mode"] ? "#202020" : "#808080";
    ctx.fillRect(this.x - sidebarW / 2, this.y, sidebarW, this.h);
    ctx.strokeRect(this.x - sidebarW / 2, this.y, sidebarW, this.h);

    if (this.title) {
      ctx.fillStyle = boolSettings["Dark Mode"] ? "#F0F0F0" : "#000000";
      ctx.font = "bold " + this.h * 0.666 + "px Arial";
      ctx.fillText(this.title, this.x, this.y + this.h * 0.75);
    }
  };
};
