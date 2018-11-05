

  // set canvas id to variable
  var canvas = document.getElementById("draw");
  var rect = canvas.getBoundingClientRect()
  canvas.style.cursor = "crosshair";
  // get canvas 2D context and set it to the correct size
  var context = canvas.getContext("2d");
  resize();


  
  // resize canvas when window is resized
  function resize() {
    // context.canvas.width = window.innerWidth;
    // context.canvas.height = window.innerHeight;
    context.canvas.width = 800;
    context.canvas.height = 800;
  }

  function clearCanvas(){
    context.clearRect(0,0,canvas.width, canvas.height);
  }

  // add event listeners to specify when functions should be triggered
  window.addEventListener("resize", resize);
  canvas.addEventListener("mousemove", draw);
  canvas.addEventListener("mousedown", setPosition);
  canvas.addEventListener("mouseenter", setPosition);

  canvas.addEventListener("touchstart", setPosition);
  canvas.addEventListener("touchmove", draw);
  canvas.addEventListener("touchend", setPosition);
  // canvas.addEventListener("touchcancel", cancel, false);

  // last known position
  var pos = { x: 0, y: 0 };

  // new position from mouse events
  function setPosition(e) {
    pos.x = (e.changedTouches ? e.changedTouches[0].pageX : e.clientX)-rect.left;
  pos.y = (e.changedTouches ? e.changedTouches[0].pageY : e.clientY)-rect.top;
// pos.x = e.clientX-rect.left;
//   pos.y = e.clientY-rect.top;
  }

  function draw(e) {
    if (e.buttons !== 1) return; // if mouse is pressed.....
    var color = "#cb3594"
    // var color = document.getElementById("hex").value;

    context.beginPath(); // begin the drawing path

    context.lineWidth = 20; // width of line
    context.lineCap = "round"; // rounded end cap
    context.strokeStyle = color; // hex color of line

    context.moveTo(pos.x, pos.y );
    // alert(pos.x) // from position
    setPosition(e);
    context.lineTo(pos.x , pos.y);
    // alert(pos.x) // to position

    context.stroke(); // draw it!


    e.preventDefault();
  };