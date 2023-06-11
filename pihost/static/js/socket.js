var socket = io.connect('http://localhost:5000');

socket.on('receiveGame', (g) => {
    game = g;
    if(game.view === 0) {
        $('.inning-view').removeClass("hidden");
        $('.scoring-view').addClass("hidden");
    }else if(game.view === 1) {
        $('.inning-view').addClass("hidden");
        $('.scoring-view').removeClass("hidden");
    }
    $('#selected-view').html(views[game.view]);
    $('.curr-inning').html(game.inning);
    $('.curr-balls').html(game.balls);
    $('.curr-strikes').html(game.strikes);
    $('.curr-outs').html(game.outs);
    $('.current-inning-points-home').html(game.board[0][game.inning - 1]);
    $('.current-inning-points-guests').html(game.board[1][game.inning - 1]);
    drawBoard();
});

socket.on('screenUpdated', (status) => {
    $('#update-screen-btn').prop('disabled', false);
    $('#update-screen-btn').html('scorebord bijwerken');
})