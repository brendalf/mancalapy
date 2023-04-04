from collections import deque
from typing import Optional

from flask_socketio import emit

from mancala_backend.core.game import MancalaGame
from mancala_backend.models import User
from mancala_backend.models.session import Session, SingleUserSession

active_sessions = dict()
users = dict()
waiting_list = deque()


def add_user_connection(user_socket_id: str) -> None:
    user = User(user_socket_id)

    users[user.socket_id] = user

    print(f"user {user_socket_id} connected")
    emit("server", {"data": "connected"}, to=user_socket_id)


def is_user_playing(user_socket_id: str) -> bool:
    if user_socket_id not in users:
        return False

    return get_user(user_socket_id).is_playing


def get_user(user_socket_id: str) -> User:
    return users[user_socket_id]


def delete_user(user_socket_id: str) -> None:
    del users[user_socket_id]


def get_session_from_user(user_socket_id: str) -> Optional[Session]:
    user = get_user(user_socket_id)
    game_id = user.current_game

    if not game_id:
        user.disconnect_from_game()
        return None

    return get_session(game_id)


def is_session_active(session_id: str) -> bool:
    return session_id in active_sessions


def get_session(session_id: str) -> Session:
    return active_sessions[session_id]


def delete_session(session_id: str) -> None:
    session = get_session(session_id)
    session.disconnect()

    del active_sessions[session_id]


def create_single_user_game(user_socket_id: str, data: dict) -> None:
    user = get_user(user_socket_id)

    session = SingleUserSession(
        user=user,
        players=[data["player1_name"], data["player2_name"]],
        game=MancalaGame(),
    )

    active_sessions[session.get_id()] = session
    session.start_session()


def create_multi_user_game(user1_socket_id: str, user2_socket_id: str) -> None:
    pass
    # user1 = users[user1_socket_id]
    # user2 = users[user2_socket_id]

    # session = MultiUserSession(
    #     users=[user1, user2],
    #     game=MancalaGame()
    # )

    # active_sessions[session.get_id()] = session
    # session.start_session()


def add_user_to_waiting_list(user_socket_id: str, _: dict) -> None:
    waiting_list.append(user_socket_id)
    match_users_in_waiting_list()


def match_users_in_waiting_list() -> None:
    while len(waiting_list) >= 2:
        user1_socket_id = waiting_list.pop()
        user2_socket_id = waiting_list.pop()

        create_multi_user_game(user1_socket_id, user2_socket_id)


def healthcheck():
    return {
        "active_sessions": [game_id for game_id in active_sessions.keys()],
        "users": [user for user in users],
        "waiting_list": [user_socket_id for user_socket_id in waiting_list],
    }
