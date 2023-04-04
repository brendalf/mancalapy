from flask import request
from flask_socketio import emit

from mancala_backend.controller import (
    add_user_connection,
    add_user_to_waiting_list,
    create_single_user_game,
    delete_session,
    delete_user,
    get_session,
    get_session_from_user,
    get_user,
    is_session_active,
    is_user_playing,
)

GAME_TYPES = {"single": create_single_user_game, "multi": add_user_to_waiting_list}


def get_socket_id() -> str:
    return request.sid


def on_connect():
    user_socket_id = get_socket_id()

    add_user_connection(user_socket_id)


def on_disconnect():
    user_socket_id = get_socket_id()

    user = get_user(user_socket_id)

    if is_user_playing(user_socket_id):
        game_id = user.current_game

        session = get_session(game_id)

        session.disconnect()

        delete_session(game_id)

    delete_user(user_socket_id)


def on_error(exception: Exception) -> None:
    print(exception)
    emit("error", {"message": str(exception)})


def on_start_game(data: dict):
    user_socket_id = get_socket_id()

    if "type" not in data:
        raise ValueError(
            "You need to provide the game type before starting a new game."
        )

    if is_user_playing(user_socket_id):
        raise ValueError("User currently playing a game. Can't start a new one.")

    game_type = data["type"]

    if game_type not in GAME_TYPES:
        raise ValueError(f"The game type {game_type} isn't available.")

    GAME_TYPES[game_type](user_socket_id, data)


def on_disconnect_game(data):
    user_socket_id = get_socket_id()
    game_id = data["game_id"]

    if not is_session_active(game_id):
        user = get_user(user_socket_id)
        user.disconnect_from_game()
        return

    session = get_session(data["game_id"])
    session.disconnect()

    delete_session(data["game_id"])


def on_plan_movement(data):
    user_socket_id = get_socket_id()

    session = get_session_from_user(user_socket_id)

    if session:
        session.get_movement_plan(data["player_id"], data["pit"])


def on_move(data):
    user_socket_id = get_socket_id()

    session = get_session_from_user(user_socket_id)

    if session:
        session.execute_player_move(user_socket_id, data["player_id"], data["pit"])
