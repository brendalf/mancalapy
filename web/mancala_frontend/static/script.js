var HOW_TO_PLAY = false;
var IN_GAME = false;
var GAME_ID = "";

var socket = io("http://127.0.0.1:8000");

socket.on("connect", function() {
    console.log("recovered?", socket.recovered);
});

socket.on("server", function(data) {
    console.log(data);
});

socket.on("game_start", function(data) {
    console.log(data);

    IN_GAME = true;
    GAME_ID = data["game_id"]

    startGame();

    updateBoard(data["board"]);
    updateMancalas(data["mancalas"]);
});

socket.on("game_disconnect", function() {
    IN_GAME = false;
    GAME_ID = ""

    disconnect();
});

function updateBoard(pits) {
    for (var playerID in pits) {
        for (var pit in pits[playerID]) {
            pitReference = playerID + "-" + pit;

            document.getElementById(pitReference).innerHTML = pits[playerID][pit];
        }
    }
}

function updateMancalas(mancalas) {
    for (var playerID in mancalas) {
        mancalaReference = "mancala-" + playerID;

        document.getElementById(mancalaReference).innerHTML = mancalas[playerID];
    }

}

function planMovement(event) {
    console.log(event);
    // socket.emit("plan_movement", { "player_id": player_id, "pit": pit });
}

function startGame() {
    var game = document.getElementById("game");
    game.style.display = "flex";

    var btStart = document.getElementById("start_game");
    btStart.style.display = "none";

    var btEnd = document.getElementById("stop_game");
    btEnd.style.display = "block";
}

function disconnect() {
    var game = document.getElementById("game");
    game.style.display = "none";

    var btStart = document.getElementById("start_game");
    btStart.style.display = "block";

    var btEnd = document.getElementById("stop_game");
    btEnd.style.display = "none";
}

function startSinglePlayerGame() {
    socket.emit("start_game", {type: "single"});
}

function disconnectFromGame() {
    if (GAME_ID === "") {
        disconnect();
    }

    socket.emit("disconnect_game", {game_id: GAME_ID});
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

