var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');

//Scorebord
const displaysWide = 7;
const displayWidth = 32;
let screen = [];

var initialBoard = [];
initialBoard[0] = [];
initialBoard[1] = [];
for(let i = 0; i < 9; i++) {
    initialBoard[0].push(0);
    initialBoard[1].push(0);
}

var game = {
    board: initialBoard,
    balls: 0,
    strikes: 0,
    outs: 0,
    inning: 1,
    view: 1
}

function clearScreen() {
    for (let i = 0; i < (Math.floor((canvas.width + 7) / 8)) * canvas.height; i++) {
        screen[i] = 255;
    }
}

function drawBoard() {
    //Set canvas background to black
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);


    //Draw board
    if(game.view === 0) {
        ctx.fillStyle = "white";
        ctx.font = "30px Helvetica";
        ctx.strokeStyle = "#FF0000";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, 32);
        ctx.lineTo(224, 32);
        for (let i = 1; i < 10; i++) {
            ctx.moveTo(20 * i, 0);
            ctx.lineTo(20 * i, 64);
            if(i <= game.inning) {
                let homePointsForInning = game.board[0][i - 1];
                if (homePointsForInning >= 0) {
                    if (homePointsForInning > 9) {
                        ctx.fillText("" + (homePointsForInning % 10), 1 + 20 * (i - 1), 28);
                        ctx.font = "12px Helvetica";
                        ctx.fillText("*", 13 + 20 * (i - 1), 10);
                        ctx.font = "30px Helvetica";
                    } else {
                        ctx.fillText(homePointsForInning, 1 + 20 * (i - 1), 28);
                    }
                }

                let guestPointsForInning = game.board[1][i - 1];
                if (guestPointsForInning >= 0) {
                    if (guestPointsForInning > 9) {
                        ctx.fillText("" + (guestPointsForInning % 10), 1 + 20 * (i - 1), 60);
                        ctx.font = "12px Helvetica";
                        ctx.fillText("*", 13 + 20 * (i - 1), 42);
                        ctx.font = "30px Helvetica";
                    } else {
                        ctx.fillText(guestPointsForInning, 1 + 20 * (i - 1), 60);
                    }
                }
            }
        }
        ctx.fillText(calculateTotalPoints(game.board[0]), 185, 28);
        ctx.fillText(calculateTotalPoints(game.board[1]), 185, 60);
        ctx.stroke();
    }else if(game.view === 1) {
        ctx.fillStyle = "white";
        ctx.font = "40px Helvetica";
        ctx.fillText(calculateTotalPoints(game.board[0]), 2, 30);
        ctx.fillText(calculateTotalPoints(game.board[1]), 2, 64);

        ctx.strokeStyle = "#FF0000";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(50, 0);
        ctx.lineTo(50, 64);
        ctx.moveTo(79, 0);
        ctx.lineTo(79, 32);
        ctx.moveTo(0,32);
        ctx.lineTo(224,32);
        ctx.moveTo(150,0);
        ctx.lineTo(150,64);
        ctx.moveTo(175,0);
        ctx.lineTo(175,64);
        ctx.stroke();

        ctx.fillStyle = "white";
        ctx.font = "30px Helvetica";
        ctx.fillText("B", 55, 25);
        for(let i = 0 ; i < 3; i++) {
            ctx.beginPath();
            if(game.balls > i) {
                ctx.arc(93 + (22 * i) , 17, 9, 0, 2 * Math.PI, false);
                ctx.fillStyle = "#FF0000";
                ctx.fill();
            }else{
                ctx.arc(93 + (22 * i) , 17, 8, 0, 2 * Math.PI, false);
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#FF0000';
                ctx.stroke();
            }
        }

        ctx.fillStyle = "white";
        ctx.fillText("S", 153, 25);
        for(let i = 0 ; i < 2; i++) {
            ctx.beginPath();
            if(game.strikes > i) {
                ctx.arc(190 + (22 * i) , 17, 9, 0, 2 * Math.PI, false);
                ctx.fillStyle = "#FF0000";
                ctx.fill();
            }else{
                ctx.arc(190 + (22 * i) , 17, 8, 0, 2 * Math.PI, false);
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#FF0000';
                ctx.stroke();
            }
        }

        ctx.fillStyle = "white";
        ctx.fillText("O", 151, 59);
        for(let i = 0 ; i < 2; i++) {
            ctx.beginPath();
            if(game.outs > i) {
                ctx.arc(190 + (22 * i) , 51, 9, 0, 2 * Math.PI, false);
                ctx.fillStyle = "#FF0000";
                ctx.fill();
            }else{
                ctx.arc(190 + (22 * i) , 51, 8, 0, 2 * Math.PI, false);
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#FF0000';
                ctx.stroke();
            }
        }

        ctx.fillStyle = "white";
        ctx.fillText("INN:" , 55, 59);
        ctx.font = "35px Helvetica";
        ctx.fillText(game.inning , 120, 59);
    }
}

function calculateTotalPoints(team) {
    let sum = team.reduce((a,b) => a + b, 0);
    return sum < 10 ? "0" + sum : sum;
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

function updateBoard() {
    clearScreen();
    for (let y = 0; y < canvas.height; y++) {
        for (let x = 0; x < canvas.width; x++) {
            let pixelData = ctx.getImageData(x, y, 1, 1).data;
            if (pixelData[0] || pixelData[1] || pixelData[2])
                setPixel(x, y);
        }
    }
    socket.emit('updateScreen',screen);
}
