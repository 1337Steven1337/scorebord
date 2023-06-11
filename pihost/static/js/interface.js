var views = [ 'Inning weergave' , 'Scoring weergave'];

$(document).ready(function() {
    clearScreen();
    drawBoard();

    //Volgende inning
    $('.next-inning').on('click', function() {
        if(game.inning + 1 <= 9)
            game.inning++;
        socket.emit('syncGame', game);
    })

    //Vorige inning
    $('.prev-inning').on('click', function() {
        if(game.inning - 1 >= 1)
            game.inning--;
        socket.emit('syncGame', game);
    })

    $('.decrease-balls').on('click', function() {
        if(game.balls > 0)
            game.balls--;
        socket.emit('syncGame', game);
    })

    $('.increase-balls').on('click', function() {
        if(game.balls + 1 <= 3)
            game.balls++;
        else {
            game.balls = 0;
            game.strikes = 0;
        }
        socket.emit('syncGame', game);
    })

    $('.decrease-strikes').on('click', function() {
        if(game.strikes > 0)
            game.strikes--;
        socket.emit('syncGame', game);
    })

    $('.increase-strikes').on('click', function() {
        if(game.strikes + 1 <= 2) {
            game.strikes++;
        } else {
            game.strikes = 0;
            game.balls = 0;
            if(game.outs + 1 <= 2) {
                game.outs++;
            } else {
                game.outs = 0;
            }
        }
        socket.emit('syncGame', game);
    })

    $('.decrease-outs').on('click', function() {
        if(game.outs > 0)
            game.outs--;
        socket.emit('syncGame', game);
    })

    $('.increase-outs').on('click', function() {
        if(game.outs + 1 <= 2)
            game.outs++;
        else {
            game.balls = 0;
            game.strikes = 0;
            game.outs = 0;
        }
        socket.emit('syncGame', game);
    })

    //Inning punten omhoog
    $('.increase-inning-points').on('click', function(event) {
        game.board[getTargetIndex(event.target)][game.inning-1] += 1;
        socket.emit('syncGame', game);
    })

    //Inning punten omlaag
    $('.decrease-inning-points').on('click', function(event) {
        if(game.board[getTargetIndex(event.target)][game.inning-1] - 1 >= 0)
            game.board[getTargetIndex(event.target)][game.inning-1] -= 1;
        socket.emit('syncGame', game);
    })

    $('#update-screen-btn').click(function() {
        $(this).prop("disabled", true);
        $(this).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Versturen...`);
        updateBoard();
    })

    $('#previous-view').on('click', function() {
        if(game.view - 1 < 0)
            game.view = views.length - 1;
        else
            game.view--;
        socket.emit('syncGame', game);
    })

    $('#next-view').on('click', function() {
        if(game.view + 1 >= views.length)
            game.view = 0;
        else
            game.view++;
        socket.emit('syncGame', game);
    })

});

function getTargetIndex(target) {
    return target.classList.contains('home') ? 0 : 1;
}