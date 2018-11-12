var canvas,ctx;
// Variables to keep track of the mouse position and left-button status
var mouseX,mouseY,mouseDown=0;
// Variables to keep track of the touch position
var touchX,touchY;
 // rounded end cap
var color = "#000000"
var indoor = 0;
var dataURL = "";
// Draws a dot at a specific position on the supplied canvas name
// Parameters are: A canvas context, the x position, the y position, the size of the dot

// Clear the canvas context using the canvas width and height
function clearCanvas(canvas,ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}
// Keep track of the mouse button being pressed and draw a dot at current location
function sketchpad_mouseDown() {
    mouseDown=1;
}
// Keep track of the mouse button being released
function sketchpad_mouseUp() {
    mouseDown=0;
    ctx.globalAlpha = 0;
    ctx.closePath()
}
// Keep track of the mouse position and draw a dot if mouse button is currently pressed
function sketchpad_mouseMove(e) {
    // Update the mouse co-ordinates when moved

    // Draw a dot if the mouse button is currently being pressed
    if (mouseDown===1) {
              ctx.beginPath();
      ctx.moveTo(mouseX, mouseY );
// alert(pos.x) // from position
            getMousePos(e);
ctx.lineTo(mouseX , mouseY);
console.log(ctx.lineWidth)
ctx.stroke();
if (ctx.globalAlpha === 0) {ctx.globalAlpha = 1;}
        // drawDot(ctx,mouseX,mouseY,5);
    }
}
// Get the current mouse position relative to the top-left of the canvas
function getMousePos(e) {
    scale = ctx.canvas.clientWidth/400;
    if (!e)
        var e = event;
    if (e.offsetX) {

        mouseX = e.offsetX/scale;
        mouseY = e.offsetY/scale;
        // mouseX = e.offsetX
        // mouseY = e.offsetY
    }
    else if (e.layerX) {
        mouseX = e.layerX/scale;
        mouseY = e.layerY/scale;

    }
 }
// Draw something when a touch start is detected
function sketchpad_touchStart() {
    // Update the touch co-ordinates
    ctx.globalAlpha = 1;
    getTouchPos();
    // drawDot(ctx,touchX,touchY,2);
    // Prevents an additional mousedown event being triggered
    if (event.touches){
        if (event.touches.length ===1){
            event.preventDefault();
        }
    }

}
// Draw something and prevent the default scrolling when touch movement is detected
function sketchpad_touchMove(e) {
    // Update the touch co-ordinates
    // During a touchmove event, unlike a mousemove event, we don't need to check if the touch is engaged, since there will always be contact with the screen by definition.
ctx.beginPath();
      ctx.moveTo(touchX, touchY );
// alert(pos.x) // from position
            getTouchPos(e);

ctx.lineTo(touchX , touchY);
ctx.stroke();
    // Prevent a scrolling action as a result of this touchmove triggering.
    event.preventDefault();
}
function sketchpad_touchEnd(){
    ctx.globalAlpha = 0;
    ctx.closePath();
}
// Get the touch position relative to the top-left of the canvas
// When we get the raw values of pageX and pageY below, they take into account the scrolling on the page
// but not the position relative to our target div. We'll adjust them using "target.offsetLeft" and
// "target.offsetTop" to get the correct values in relation to the top left of the canvas.
function getTouchPos(e) {
    scale = ctx.canvas.clientWidth/400;
    if (!e)
        var e = event;
    if(e.touches) {
        if (e.touches.length === 1) { // Only deal with one finger
            var touch = e.touches[0]; // Get the information for finger #1
            touchX=(touch.pageX-touch.target.offsetLeft)/scale;
            touchY=(touch.pageY-touch.target.offsetTop)/scale;

        }
    }
}

function loadBackground(element) {

    database.collection("images").doc("0").get().then(function (doc) {
        if (doc.exists) {
            var remainingImages = (doc.data().images);
            console.log(remainingImages);
            if (!(remainingImages.length)) {
                element.src = "data/done.jpg";
            }
            else {
                element.src = "data/elyseemusee_400/" + remainingImages[0];

            }

        }
        else {
            console.log("No doc")
        }
    }).catch(function (error) {
        console.log("Error", error);
    });}

    function writeInOutUserData(imageId, indoor, outdoor, dataURL) {
  database.collection("data").doc(imageId).set({
    indoor: indoor,
      dataURL: dataURL,
  });
}
function ioButton(){
      if (event.target.value === "Indoor"){
        indoor = 1;
        outdoor = 0;
        document.getElementById("indoor").style.backgroundColor = "gray";
        document.getElementById("outdoor").style.backgroundColor = "#eee";
    }
    else {
        indoor = 0;
        outdoor = 1;
        document.getElementById("outdoor").style.backgroundColor = "gray";
        document.getElementById("indoor").style.backgroundColor = "#eee";

    }
}

function nextImage(){
// only change pictures when indoor or outdoor is clicked
    if (indoor || outdoor) {
        document.getElementById("done").style.backgroundColor = "gray";
        var background = (document.getElementById("background"));
        var matches = (background.src).match(/\d+/g);
        var imageId = matches[matches.length - 1];
        console.log(imageId);
        dataURL = canvas.toDataURL("image/png");
        try {
            writeInOutUserData(imageId, indoor, dataURL);

        }
        catch (err) {
            writeInOutUserData(imageId, indoor, "");

        }




        //get the remaining images
        loadBackground(background);
        indoor = 0;
        outdoor = 0;
        clearCanvas(canvas, ctx)


        database.collection("images").doc("0").get().then(function (doc) {
        if (doc.exists) {
            var remainingImages = (doc.data().images);
            console.log(remainingImages);
            database.collection("images").doc("0").set({
                    images: remainingImages.slice(1)
                });


        }
        else {
            console.log("No doc")
        }
    }).catch(function (error) {
        console.log("Error", error);
    });

    }

    document.getElementById("done").style.backgroundColor = "#eee";
}

// Set-up the canvas and add our event handlers after the page has loaded
function init() {
    // Get the specific canvas element from the HTML document
    canvas = document.getElementById('sketchpad');
    canvas.style.cursor = "crosshair";
    // If the browser supports the canvas tag, get the 2d drawing context for this canvas
    if (canvas.getContext) {
        ctx = canvas.getContext('2d');
    }
    // Check that we have a valid context to draw on/with before adding event handlers
    if (ctx) {
        // React to mouse events on the canvas, and mouseup on the entire document
        canvas.addEventListener('mousedown', sketchpad_mouseDown, false);
        canvas.addEventListener('mousemove', sketchpad_mouseMove, false);
        window.addEventListener('mouseup', sketchpad_mouseUp, false);
        // React to touch events on the canvas
        canvas.addEventListener('touchstart', sketchpad_touchStart, false);
        canvas.addEventListener('touchmove', sketchpad_touchMove, false);
        canvas.addEventListener('touchend', sketchpad_touchEnd, false);
    }
    var background = document.getElementById("background");
    loadBackground(background);

// ctx.size = 500;

    ctx.lineWidth = 5; // width of line
    ctx.lineCap = "round";
    ctx.strokeStyle = color;
    ctx.globalAlpha = 0;
}