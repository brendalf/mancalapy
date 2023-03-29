var HOW_TO_PLAY = false;

var socket = io("http://127.0.0.1:8000");

socket.on("connect", function() {
    console.log("recovered?", socket.recovered);
});

socket.on("server", function(data) {
    console.log(data);
});

function startSinglePlayerGame() {
    socket.emit("start_game", {type: "single"});
}

function showHowToPlay() {
    var section = document.getElementById("how-to-play");

    if (HOW_TO_PLAY == false) {
        section.style.display = "block";
        HOW_TO_PLAY = true;
    } else {
        section.style.display = "none";
        HOW_TO_PLAY = false;
    }
}

function myFunction() {
    socket.emit("plan_move", {game: "game_id", player: 0, pit: 1});
}

