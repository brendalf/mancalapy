from collections import deque

from flask_socketio import close_room, disconnect, emit
from mancala_backend.controller import add_player_connection, get_socket_id, is_player_in_game, create_single_player_game, add_player_to_waiting_list
from mancala_backend.core.pit import PitReference

active_games = dict()
players = dict()
waiting_list = deque()

game_types = {
    "single": create_single_player_game,
    "multi": add_player_to_waiting_list 
}


def on_connect():
    player_socket_id = get_socket_id()

    add_player_connection(player_socket_id)

    print(f"user {player_socket_id} connected")
    emit("server", {"data": "connected"}, to=player_socket_id)


def on_start_game(data: dict):
    player_socket_id = get_socket_id()

    if "type" not in data:
        raise ValueError("You need to provide the game type before starting a new game.")

    if is_player_in_game(player_socket_id):
        raise ValueError("User currently playing a game. Can't start a new one.")

    game_type = data["type"]

    if game_type not in game_types:
        raise ValueError(f"The game type {game_type} isn't available.")

    game_types[game_type](player_socket_id)


def on_disconnect_game():
    player_socket_id = get_socket_id()
    player = players[player_socket_id]

    # TODO: get which game the player is currently in
    # TODO: call game controller disconnect


def on_plan_movement(data):
    player_socket_id = get_socket_id()
    player = players[player_socket_id]
    game_id = player.current_game
    game = active_games[game_id]

    movement = game.calculate_movement_plan(PitReference(data["player_id"], data["pit"]))

    payload = {
        "game_type": "single",
        "game_id": game.get_game_id(),
        "board": game.board.pits,
        "mancalas": game.board.mancalas,
        "movement": movement
    }

    emit("server", payload)


def on_disconnect():
    player_socket_id = get_socket_id()
    player = players[player_socket_id]

    if player.is_playing:
        game_id = player.current_game

        game = active_games[game_id]

        game.disconnect()

        del active_games[game_id]

    if player_socket_id in players:
        del players[player_socket_id]
        print(f"removing user {player_socket_id}")

    print(f"user {player_socket_id} disconnected")

    emit("server", {"data": "disconnected"}, to=player_socket_id)
