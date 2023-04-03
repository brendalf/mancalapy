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

    player1 = document.getElementById("label-0");
    player1.innerHTML = data["player1"];

    player2 = document.getElementById("label-1");
    player2.innerHTML = data["player2"];

    updateBoard(data["board"]);
    updateMancalas(data["mancalas"]);
});

socket.on("game_disconnect", function() {
    IN_GAME = false;
    GAME_ID = ""

    disconnect();
});

socket.on("plan_movement", function(data) {
    data["movement"].forEach(function(item) {
        elementId = item["player_id"] + "-" + item["position"];
        pit = document.getElementById(elementId);
        pit.classList.add("highlight");
    });

    if (data["captured_stones"] > 0) {
        mancala = document.getElementById("mancala-0");
        mancala.classList.add("highlight");
    }
});


socket.on("update_game", function(data) {
    updateBoard(data["board"]);
    updateMancalas(data["mancalas"]);
})

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

function planMovement(element) {
    var id = element.id.split("-");
    var player_id = id[0];
    var pit = id[1];
    socket.emit("plan_movement", { "player_id": player_id, "pit": pit });
}

function removePitHighlight() {
    selection = document.getElementsByClassName("highlight");
    elements_with_highlight = [];

    for(var i = 0; i < selection.length; i++) {
        elements_with_highlight.push(selection[i]);
    }

    for(var i = 0; i < elements_with_highlight.length; i++) {
        item = elements_with_highlight[i];
        item.classList.remove("highlight");
    }
}

function startGame() {
    var game = document.getElementById("game");
    game.style.display = "flex";

    var btStart = document.getElementById("start_game");
    btStart.style.display = "none";

    var btStart = document.getElementById("start_online_game");
    btStart.style.display = "none";

    var btEnd = document.getElementById("stop_game");
    btEnd.style.display = "block";
}

function disconnect() {
    var game = document.getElementById("game");
    game.style.display = "none";

    var btStart = document.getElementById("start_game");
    btStart.style.display = "block";

    var btStart = document.getElementById("start_online_game");
    btStart.style.display = "block";

    var btEnd = document.getElementById("stop_game");
    btEnd.style.display = "none";
}

function startLocalGame() {
    p1_name = prompt("Enter player one name:");
    p2_name = prompt("Enter player two name:");

    socket.emit("start_game", {type: "single", player1_name: p1_name, player2_name: p2_name});
}

function startOnlineGame() {
    console.log("WIP");
}

function disconnectFromGame() {
    console.log(GAME_ID);

    if (GAME_ID === "") {
        disconnect();
    }

    socket.emit("disconnect_game", {game_id: GAME_ID});
}

function toggleHowToPlaySection() {
    var section = document.getElementById("how-to-play");

    if (HOW_TO_PLAY === false) {
        section.style.display = "block";
        HOW_TO_PLAY = true;
    } else {
        section.style.display = "none";
        HOW_TO_PLAY = false;
    }
}

function movePit(element) {
    var id = element.id.split("-");
    var player_id = id[0];
    var pit = id[1];
    socket.emit("move", { "player_id": player_id, "pit": pit });
}
