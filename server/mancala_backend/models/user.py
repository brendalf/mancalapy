from dataclasses import dataclass
from typing import Optional

from flask_socketio import emit


@dataclass()
class User:
    socket_id: str
    current_game: Optional[str] = None
    is_playing: Optional[bool] = False

    def set_current_game(self, game_id: str) -> None:
        self.is_playing = True
        self.current_game = game_id

    def disconnect_from_game(self) -> None:
        self.is_playing = False
        self.current_game = None

        emit("disconnect_game", to=self.socket_id)
