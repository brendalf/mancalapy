from collections import deque

from flask import request
from flask_socketio import emit, join_room
from mancala_backend.models.game import Game
from mancala_backend.models.player import Player
from mancala_backend.core import MancalaGame

active_games = dict()
players = dict()
waiting_list = deque()


def get_socket_id() -> str:
    return request.sid


def add_player_connection(player_socket_id: str) -> None:
    player = Player(player_socket_id)

    players[player.socket_id] = player


def is_player_in_game(player_id: str) -> bool:
    if player_id not in players:
        return False

    return players[player_id].is_playing


def create_single_player_game(player_socket_id: str) -> None:
    player = players[player_socket_id]

    game = MancalaGame() 

    player.set_current_game(game.id)

    active_games[game.get_game_id()] = game

    emit("server", {"game_id": game.get_game_id()})


def create_multi_player_game(player_id_0: str, player_id_1: str) -> None:
    player0 = players[player_id_0]
    player1 = players[player_id_1]

    # game = Game(p0, p1)

    # join_room(game.game_id, p0.socket_id)
    # join_room(game.game_id, p1.socket_id)

    # emit("server", {"data": f"starting game {game.game_id}"}, to=game.game_id)

    # print(f"starting game {game.game_id}: {p0} x {p1}")

    # active_games[game.game_id] = game

    return None


def add_player_to_waiting_list(player_socket_id: str) -> None:
    waiting_list.append(player_socket_id)
    match_players_in_waiting_list()


def match_players_in_waiting_list() -> None:
    while len(waiting_list) >= 2:
        player_id_0 = waiting_list.pop()
        player_id_1 = waiting_list.pop()

        create_multi_player_game(player_id_0, player_id_1)


def healthcheck():
    return {
        "active_games": {
            game_id: (game.player_one, game.player_two)
            for game_id, game in active_games.items()
        },
        "players": [player for player in players],
        "waiting_list": [id for id in waiting_list],
    }
