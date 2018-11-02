
// set canvas id to variable
var canvas = document.getElementById("draw");
var rect = canvas.getBoundingClientRect()
canvas.style.cursor = "crosshair";
// get canvas 2D context and set it to the correct size
var ctx = canvas.getContext("2d");
resize();

// resize canvas when window is resized
function resize() {
  // ctx.canvas.width = window.innerWidth;
  // ctx.canvas.height = window.innerHeight;
  ctx.canvas.width = 800;
  ctx.canvas.height = 800;
}

// add event listeners to specify when functions should be triggered
window.addEventListener("resize", resize);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mousedown", setPosition);
canvas.addEventListener("mouseenter", setPosition);

canvas.addEventListener("touchstart", setPosition);
canvas.addEventListener("touchmove", draw);
canvas.addEventListener("touchend", setPosition);


// last known position
var pos = { x: 0, y: 0 };

// new position from mouse events
function setPosition(e) {
  pos.x = e.clientX - rect.left;
  pos.y = e.clientY - rect.top;
}

function draw(e) {
  if (e.buttons !== 1) return; // if mouse is pressed.....

  var color = document.getElementById("hex").value;

  ctx.beginPath(); // begin the drawing path

  ctx.lineWidth = 20; // width of line
  ctx.lineCap = "round"; // rounded end cap
  ctx.strokeStyle = color; // hex color of line

  ctx.moveTo(pos.x, pos.y ); // from position
  setPosition(e);
  ctx.lineTo(pos.x , pos.y); // to position

  ctx.stroke(); // draw it!
}