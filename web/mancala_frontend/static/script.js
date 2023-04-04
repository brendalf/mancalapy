let HOW_TO_PLAY = false;
let IN_GAME = false;
let GAME_ID = "";
let CURRENT_PLAYER = 0;

const socket = io("http://127.0.0.1:8000");
const server_status = document.getElementById("server_status");

socket.on("connect", () => {
    server_status.innerText = "Server: Connected";
});

socket.on("disconnect", () => {
    server_status.innerText = "Server: Disconnected";
});

socket.on("connect_error", () => {
    server_status.innerText = "Server: Connection Error";
});

socket.on("error", (data) => {
    alert(data["message"]);
});

socket.on("server", (data) => {
	console.log(data);
});

socket.on("game_start", (data) => {
	console.log(data);

	IN_GAME = true;
	GAME_ID = data.game_id;
	CURRENT_PLAYER = data.player1;

	displayGameSection();

	updateTurnDisplay();

	const player1 = document.getElementById("label-0");
	player1.innerHTML = data.player1;

	const player2 = document.getElementById("label-1");
	player2.innerHTML = data.player2;

	enableCurrentPlayerPits();

	updateBoard(data.board);
	updateMancalas(data.mancalas);
});

socket.on("game_disconnect", () => {
	IN_GAME = false;
	GAME_ID = "";
	hideGameSection();
});

socket.on("plan_movement", (data) => {
	console.log(data);

	data.movement.forEach((item) => {
		const elementId = `${item.player_id}-${item.position}`;
		const pit = document.getElementById(elementId);
		pit.classList.add("highlight");
	});

	if (data.captured_stones > 0) {
		const currentPlayer = CURRENT_PLAYER === "breno" ? 0 : 1;
		const mancala = document.getElementById(`mancala-${currentPlayer}`);
		mancala.classList.add("highlight");
	}
});

socket.on("update_game", (data) => {
	updateBoard(data.board);
	updateMancalas(data.mancalas);

	CURRENT_PLAYER = "tomas";
	enableCurrentPlayerPits();
	updateTurnDisplay();
});

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

function planMovement(event) {
	const id = event.target.id.split("-");
	const player_id = id[0];
	const pit = id[1];
	socket.emit("plan_movement", { player_id, pit });
}

function removePitHighlight() {
	const elementsWithHighlight = document.querySelectorAll(".highlight");
	elementsWithHighlight.forEach((item) => {
		item.classList.remove("highlight");
	});
}

function enableCurrentPlayerPits() {
	const currentPlayer = CURRENT_PLAYER === "breno" ? 0 : 1;

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

function movePit(event) {
    removePitHighlight();

    var id = event.target.id.split("-");
    var player_id = id[0];
    var pit = id[1];
    socket.emit("move", { "player_id": player_id, "pit": pit });
}
