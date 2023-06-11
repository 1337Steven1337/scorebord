var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
var socket = io.connect('http://localhost:5000');

//Scorebord
var board = [];
board[0] = [];
board[1] = [];
for(let i = 0; i < 9; i++) {
    board[0].push(0);
    board[1].push(0);
}

function drawBoard() {
    //Set canvas background to black
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    //Draw board
    ctx.fillStyle = "white";
    ctx.font = "30px Helvetica";
    ctx.strokeStyle = "#FF0000";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0,32);
    ctx.lineTo(224,32);
    for(let i = 1; i < 10; i++) {
        ctx.moveTo(20*i,0);
        ctx.lineTo(20*i,64);
        ctx.fillText("" + board[0][i-1], 1 + 20*(i-1), 28);
        ctx.fillText("" + board[1][i-1], 1 + 20*(i-1), 60);
    }
    ctx.fillText(calculateTotalPoints(board[0]), 185, 28);
    ctx.fillText(calculateTotalPoints(board[1]), 185, 60);
    ctx.stroke();
}

function calculateTotalPoints(team) {
    let sum = team.reduce((a,b) => a + b, 0);
    return sum < 10 ? "0" + sum : sum;
}

//Scorebord kenmerken
const displaysWide = 7;
const displaysHigh = 4;
const displayWidth = 32;
const displayHeight = 16;
const displaysTotal = displaysWide * displaysHigh;

//Teken spul
let mousePressed = false;
let lastX, lastY;
let screen = [];

$(document).ready(function() {
    drawBoard();

    for(let i = 0; i < (Math.floor((canvas.width+7) / 8)) * canvas.height; i++) {
        screen[i] = 255;
    }

    $('#myCanvas').mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });
    $('#myCanvas').mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });
    $('#myCanvas').mouseup(function (e) {
        mousePressed = false;
    });
    $('#myCanvas').mouseleave(function (e) {
        mousePressed = false;
    });
});

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        ctx.strokeStyle = "#FFFFFF";
        ctx.lineWidth = 2;
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x; lastY = y;
}

function clearArea() {
    for(let i = 0; i < (Math.floor((canvas.width+7) / 8)) * canvas.height; i++) {
        screen[i] = 255;
    }
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function pixelToBitmapIndex(x,y) {
    return parseInt(Math.floor((y * (displayWidth * displaysWide) + x) / 8));
}

function setPixel(x,y) {
    if(x>= canvas.width || y >= canvas.height)
        return;
    let byteIndex = pixelToBitmapIndex(x,y);
    screen[byteIndex] &= ~(0x80 >> (x & 0x07));
}

/*function diff() {
    screenDiff = [];
    for(let y = 0 ; y < canvas.height; y++){
        for( let x = 0; x < canvas.width; x++){
            let oldPixel = ctx.getImageData(x, y, 1, 1);
            let pixelData = ctx.getImageData(x, y, 1, 1).data;
            let pixelData2 = ctx2.getImageData(x, y, 1, 1).data;
            if(pixelData[0] !== pixelData2[0]
            || pixelData[1] !== pixelData2[1]
            || pixelData[2] !== pixelData2[2]) {
                ctx2.putImageData(oldPixel, x, y);
                screenDiff.push({x: x, y:y });
            }else{
                let newPixel = ctx2.createImageData(1,1);
                let newPixelData = newPixel.data;
                newPixelData[0] = newPixelData[1] = newPixelData[2] = 0;
                newPixelData[3] = 255;
                ctx2.putImageData(newPixel,x,y);
            }
        }
    }
    console.log(screenDiff);
}*/

function convert() {
    for(let y = 0 ; y < canvas.height; y++){
        for( let x = 0; x < canvas.width; x++){
            let pixelData = ctx.getImageData(x, y, 1, 1).data;
            if(pixelData[0] || pixelData[1] || pixelData[2] )
                setPixel(x,y);
        }
    }
}

function send() {
    socket.emit('updateBoard',screen);
}
