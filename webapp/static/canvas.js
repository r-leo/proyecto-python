// =============
// == Globals ==
// =============
const canvas = document.getElementById('drawing-area');
const canvasContext = canvas.getContext('2d');
const clearButton = document.getElementById('clear-button');
const processButton = document.getElementById('process-button');
const state = {
  mousedown: false
};

const width = $(document).width();

if (width > 500) {
  canvas.width  = 400;
  canvas.height = 400;
}
else {
  canvas.width  = Math.round(0.8 * width);
  canvas.height = Math.round(0.8 * width);
}

size = canvas.width;

function getBoundingBox(ctx, left, top, width, height) {
    var ret = {};

    // Get the pixel data from the canvas
    var data = ctx.getImageData(left, top, width, height).data;
    //console.log(data);
    var first = false;
    var last = false;
    var right = false;
    var left = false;
    var r = height;
    var w = 0;
    var c = 0;
    var d = 0;

    // 1. get bottom
    while(!last && r) {
        r--;
        for(c = 0; c < width; c++) {
            if(data[r * width * 4 + c * 4 + 3]) {
                //console.log('last', r);
                last = r+1;
                ret.bottom = r+1;
                break;
            }
        }
    }

    // 2. get top
    r = 0;
    var checks = [];
    while(!first && r < last) {

        for(c = 0; c < width; c++) {
            if(data[r * width * 4 + c * 4 + 3]) {
                //console.log('first', r);
                first = r-1;
                ret.top = r-1;
                ret.height = last - first - 1;
                break;
            }
        }
        r++;
    }

    // 3. get right
    c = width;
    while(!right && c) {
        c--;
        for(r = 0; r < height; r++) {
            if(data[r * width * 4 + c * 4 + 3]) {
                //console.log('last', r);
                right = c+1;
                ret.right = c+1;
                break;
            }
        }
    }

    // 4. get left
    c = 0;
    while(!left && c < right) {

        for(r = 0; r < height; r++) {
            if(data[r * width * 4 + c * 4 + 3]) {
                //console.log('left', c-1);
                left = c;
                ret.left = c;
                ret.width = right - left - 1;
                break;
            }
        }
        c++;

        // If we've got it then return the height
        if(left) {
        	return ret;
        }
    }

    // We screwed something up...  What do you expect from free code?
    return false;
}

function procesar() {
  var bbox = getBoundingBox(canvasContext, 0, 0, size, size);
  if (!bbox) {
    console.log('<canvas> vacío.');
  }
  else {
    $('#container').children().hide();
    $('#cargando').css('display', 'flex');
    $.redirect('/procesar', {
      'img': canvas.toDataURL(),
      'l': bbox.left,
      't': bbox.top,
      'b': bbox.bottom,
      'r': bbox.right,
      'w': bbox.width,
      'h': bbox.height
    });
  }
}

// ===================
// == Configuration ==
// ===================
const lineWidth = size / 10;
//const halfLineWidth = lineWidth / 2;
const halfLineWidth = 0;
const fillStyle = '#333';
const strokeStyle = '#333';
const shadowColor = '#333';
//const shadowBlur = lineWidth / 4;
const shadowBlur = 0;

// =====================
// == Event Listeners ==
// =====================
canvas.addEventListener('mousedown', handleWritingStart);
canvas.addEventListener('mousemove', handleWritingInProgress);
canvas.addEventListener('mouseup', handleDrawingEnd);
canvas.addEventListener('mouseout', handleDrawingEnd);

canvas.addEventListener('touchstart', handleWritingStart);
canvas.addEventListener('touchmove', handleWritingInProgress);
canvas.addEventListener('touchend', handleDrawingEnd);

clearButton.addEventListener('click', handleClearButtonClick);
processButton.addEventListener('click', procesar);

// ====================
// == Event Handlers ==
// ====================
function handleWritingStart(event) {
  event.preventDefault();

  const mousePos = getMosuePositionOnCanvas(event);

  canvasContext.beginPath();

  canvasContext.moveTo(mousePos.x, mousePos.y);

  canvasContext.lineWidth = lineWidth;
  canvasContext.strokeStyle = strokeStyle;
  canvasContext.shadowColor = null;
  canvasContext.shadowBlur = null;

  canvasContext.fill();

  state.mousedown = true;
}

function handleWritingInProgress(event) {
  event.preventDefault();

  if (state.mousedown) {
    const mousePos = getMosuePositionOnCanvas(event);

    canvasContext.lineTo(mousePos.x, mousePos.y);
    canvasContext.stroke();
  }
}

function handleDrawingEnd(event) {
  event.preventDefault();

  if (state.mousedown) {
    canvasContext.shadowColor = shadowColor;
    canvasContext.shadowBlur = shadowBlur;

    canvasContext.stroke();
  }

  state.mousedown = false;
}

function handleClearButtonClick(event) {
  event.preventDefault();

  clearCanvas();
}

// ======================
// == Helper Functions ==
// ======================
function getMosuePositionOnCanvas(event) {
  const clientX = event.clientX || event.touches[0].clientX;
  const clientY = event.clientY || event.touches[0].clientY;
  const { offsetLeft, offsetTop } = event.target;
  const canvasX = clientX - offsetLeft;
  const canvasY = clientY - offsetTop;

  return { x: canvasX, y: canvasY };
}

function clearCanvas() {
  canvasContext.clearRect(0, 0, canvas.width, canvas.height);
}
