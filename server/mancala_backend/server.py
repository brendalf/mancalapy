from typing import Tuple

from mancala_backend.controller import healthcheck
from mancala_backend.events import on_connect, on_disconnect, on_start_game
from flask import Flask
from flask_socketio import SocketIO


def create_server() -> Tuple[Flask, SocketIO]:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some-super-secret-key'

    socket = SocketIO(app, cors_allowed_origins=["http://localhost:8080"], logger=True, engineio_logger=True)

    return app, socket


def define_socket_routes(socket: SocketIO) -> None:
    socket.on_event("connect", on_connect)
    socket.on_event("disconnect", on_disconnect)
    socket.on_event("start_game", on_start_game)


def define_routes(app: Flask) -> None:
    app.add_url_rule(rule="/healthcheck", view_func=healthcheck)
