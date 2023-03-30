from dataclasses import dataclass
from typing import Optional


@dataclass()
class Player:
    socket_id: str
    current_game: Optional[str] = None
    is_playing: Optional[bool] = False

    def set_current_game(self, game_id: str) -> None:
        self.is_playing = True
        self.current_game = game_id
