// **************************
// **** GLOBAL VARIABLES ****
// **************************
let HOW_TO_PLAY = false;
let IN_GAME = false;
let GAME_ID = "";
let CURRENT_PLAYER = 0;

const socket = io("http://127.0.0.1:8000");
const server_status = document.getElementById("server_status");

// **************************
// ****      SOCKET      ****
// **************************
socket.on("connect", () => {
    server_status.innerText = "Server: Connected";

    document.getElementById("start_game").classList.remove("disabled");
});

socket.on("disconnect", () => {
    server_status.innerText = "Server: Disconnected";

    IN_GAME = false;
    GAME_ID = "";

    document.getElementById("start_game").classList.add("disabled");

    displayMenu();
});

socket.on("connect_error", () => {
    server_status.innerText = "Server: Connection Error";

    IN_GAME = false;
    GAME_ID = "";

    document.getElementById("start_game").classList.add("disabled");

    displayMenu();
});

socket.on("error", (data) => {
    alert(data["message"]);
});

socket.on("server", (data) => {
	console.log(data);
});

socket.on("update_game", (data) => {
	console.log(data);

    IN_GAME = true;
    GAME_ID = data["game_id"];

    const players = data["players"];

    for(let i = 0; i < players.length; i++) {
        const element = document.getElementById(`label-${i}`);
        element.innerText = players[i];
    }

    displayGameSection();
	updateBoard(data.board);
	updateMancalas(data.mancalas);

    CURRENT_PLAYER = data["players"][data["current_player"]];

    // Update state and view
    if(data["game_state"] === "GAME_FINISHED") {
        const display = document.getElementById("status");
        display.innerHTML = `Winner: ${data["winner"]}`;
    }
    
    if(data["game_state"] === "IN_GAME") {
        enableCurrentPlayerPits(data["current_player"]);
        updateTurnDisplay();
    }
});

socket.on("disconnect_game", () => {
	IN_GAME = false;
	GAME_ID = "";
	hideGameSection();
});

socket.on("plan_movement", (data) => {
	data.movement.forEach((item) => {
		const elementId = `${item.player_id}-${item.position}`;
		const pit = document.getElementById(elementId);
		pit.classList.add("highlight");
	});

	if (data.captured_stones > 0) {
		const mancala = document.getElementById(`mancala-${data["current_player"]}`);
		mancala.classList.add("highlight");
	}
});

// **************************
// ****   USER ACTIONS   ****
// **************************
function startLocalGame() {
    p1_name = prompt("Enter player one name:");
    p2_name = prompt("Enter player two name:");

    socket.emit("start_game", {type: "single", player1_name: p1_name, player2_name: p2_name});
}

function startOnlineGame() {
    alert("This is still a working in progress");
}

function disconnectFromGame() {
    if (GAME_ID === "") {
        hideGameSection();
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

function planMovement(event) {
	const id = event.target.id.split("-");
	const player_id = id[0];
	const pit = id[1];
	socket.emit("plan_movement", { player_id, pit });
}

function movePit(event) {
    removePitHighlight();

    var id = event.target.id.split("-");
    var pit = id[1];
    socket.emit("move", { "player_id": CURRENT_PLAYER, "pit": pit });
}

// **************************
// **** UPDATE GAME VIEW ****
// **************************
function updateTurnDisplay() {
	const display = document.getElementById("status");
	display.innerHTML = `Current player: ${CURRENT_PLAYER}`;
}

function updateBoard(playerPits) {
	for (const playerIndex in playerPits) {
		for (const pit in playerPits[playerIndex]) {
			const pitReference = `${playerIndex}-${pit}`;
			document.getElementById(pitReference).innerHTML = playerPits[playerIndex][pit];
		}
	}
}

function updateMancalas(mancalas) {
	for (const playerID in mancalas) {
		const mancalaReference = `mancala-${playerID}`;
		document.getElementById(mancalaReference).innerHTML = mancalas[playerID];
	}
}

function removePitHighlight() {
	const elementsWithHighlight = document.querySelectorAll(".highlight");
	elementsWithHighlight.forEach((item) => {
		item.classList.remove("highlight");
	});
}

function enableCurrentPlayerPits(currentPlayer) {
	// remove the "active" class
	const allPits = document.querySelectorAll(".pit.active");
	allPits.forEach((item) => {
		item.classList.remove("active");
		item.removeEventListener("click", movePit);
		item.removeEventListener("mouseover", planMovement);
		item.removeEventListener("mouseout", removePitHighlight);
	});

	// add the "active" class to the current player's pits
	const currentPits = document.querySelectorAll(`.pit.player-${currentPlayer}`);
	currentPits.forEach((item) => {
		item.classList.add("active");
		item.addEventListener("click", movePit);
		item.addEventListener("mouseover", planMovement);
		item.addEventListener("mouseout", removePitHighlight);
	});
}

function displayGameSection() {
    const game = document.getElementById("game");
    game.style.display = "flex";

    const btStart = document.getElementById("start_game");
    btStart.style.display = "none";

    const btOnlineStart = document.getElementById("start_online_game");
    btOnlineStart.style.display = "none";

    const btEnd = document.getElementById("stop_game");
    btEnd.style.display = "block";
}

function displayMenu() {
    const game = document.getElementById("game");
    game.style.display = "none";

    const btStart = document.getElementById("start_game");
    btStart.style.display = "block";

    const btOnlineStart = document.getElementById("start_online_game");
    btOnlineStart.style.display = "block";

    const btEnd = document.getElementById("stop_game");
    btEnd.style.display = "none";
}
