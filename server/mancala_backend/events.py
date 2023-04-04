from collections import deque

from flask_socketio import close_room, disconnect, emit

from mancala_backend.controller import (
    add_player_connection,
    add_player_to_waiting_list,
    create_single_player_game,
    delete_game,
    get_active_game,
    get_player,
    get_socket_id,
    is_player_in_game,
)
from mancala_backend.core.pit import PitReference

game_types = {"single": create_single_player_game, "multi": add_player_to_waiting_list}


def on_connect():
    player_socket_id = get_socket_id()

    add_player_connection(player_socket_id)

    print(f"user {player_socket_id} connected")
    emit("server", {"data": "connected"}, to=player_socket_id)


def on_start_game(data: dict):
    player_socket_id = get_socket_id()

    if "type" not in data:
        raise ValueError(
            "You need to provide the game type before starting a new game."
        )

    if is_player_in_game(player_socket_id):
        raise ValueError("User currently playing a game. Can't start a new one.")

    game_type = data["type"]

    if game_type not in game_types:
        raise ValueError(f"The game type {game_type} isn't available.")

    game_types[game_type](player_socket_id, data)


def on_disconnect_game(data):
    delete_game(data["game_id"])

    # TODO: get which game the player is currently in
    # TODO: call game controller disconnect

    emit("game_disconnect")


def on_plan_movement(data):
    player_socket_id = get_socket_id()
    player = get_player(player_socket_id)

    # TODO: temporarily
    if not player.current_game:
        return

    game_id = player.current_game
    game = get_active_game(game_id)

    pit = PitReference(int(data["player_id"]), int(data["pit"]))
    movement = game.calculate_movement_plan(pit)

    plan = [
        {"player_id": pit_reference.player_id, "position": pit_reference.position}
        for pit_reference in movement[0]
    ]

    payload = {
        "game_type": "single",
        "game_id": game.get_game_id(),
        "movement": plan,
        "captured_stones": movement[1],
    }

    emit("plan_movement", payload)


def on_error(exception: Exception) -> None:
    print(exception)
    emit("error", {"message": str(exception)})


def on_move(data):
    player_socket_id = get_socket_id()
    player = get_player(player_socket_id)

    # TODO: temporarily
    if not player.current_game:
        return

    game_id = player.current_game
    game = get_active_game(game_id)

    player_id = int(data["player_id"])
    pit_position = int(data["pit"])

    game.execute_player_movement(player_id, pit_position)

    payload = {
        "game_type": "single",
        "game_id": game.get_game_id(),
        "board": game.board.pits,
        "mancalas": game.board.mancalas,
    }

    emit("update_game", payload)


def on_disconnect():
    player_socket_id = get_socket_id()

    player = get_player(player_socket_id)

    if player.is_playing:
        game_id = player.current_game

        game = get_active_game(game_id)

        # game.disconnect()

        delete_game(game_id)

    # if player_socket_id in players:
    #     del players[player_socket_id]
    #     print(f"removing user {player_socket_id}")

    print(f"user {player_socket_id} disconnected")

    emit("server", {"data": "disconnected"}, to=player_socket_id)
