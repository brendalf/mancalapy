from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Protocol

from flask_socketio import emit

from mancala_backend.core.game import MancalaGame
from mancala_backend.core.pit import PitReference
from mancala_backend.models.user import User


class SessionState(Enum):
    WAITING_TO_START = 0
    IN_GAME = 1
    GAME_FINISHED = 2


class Session(Protocol):
    def start_session(self) -> None:
        ...

    def get_id(self) -> str:
        ...

    def sync_game_state(self) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def get_movement_plan(self, player_number: int, pit_position: int) -> None:
        ...

    def execute_player_move(
        self, socket_id: str, player_moving: str, pit_position: int
    ):
        ...


@dataclass
class SingleUserSession:
    user: User
    players: List[str]
    game: MancalaGame
    state: SessionState = field(init=False)

    def __post_init__(self) -> None:
        self.state = SessionState.WAITING_TO_START

    def start_session(self) -> None:
        self.state = SessionState.IN_GAME

        self.user.set_current_game(self.game.get_game_id())

        self.sync_game_state()

    def sync_game_state(self) -> None:
        payload = self._get_game_payload()

        if self.game.has_game_ended():
            self.game.finish()
            self.state = SessionState.GAME_FINISHED

            payload["game_state"] = self.state.name
            payload["winner"] = self.players[self.game.get_winner()]

        emit("update_game", payload, to=self.user.socket_id)

    def get_id(self) -> str:
        return self.game.get_game_id()

    def disconnect(self) -> None:
        self.user.disconnect_from_game()

    def get_player_number(self, player: str) -> int:
        try:
            number = self.players.index(player)
            return number
        except ValueError:
            raise ValueError(f"There is no player with name: {player}")

    def execute_player_move(
        self, socket_id: str, player_moving: str, pit_position: int
    ):
        if self.user.socket_id != socket_id:
            raise ValueError(
                f"User {socket_id} isn't allowed to interact with game {self.game.get_game_id()}."
            )

        player_number = self.get_player_number(player_moving)

        self.game.execute_player_movement(player_number, int(pit_position))

        self.sync_game_state()

    def get_movement_plan(self, player_number: int, pit_position: int) -> None:
        pit_reference = PitReference(int(player_number), int(pit_position))
        movement = self.game.calculate_movement_plan(pit_reference)

        plan = [
            {"player_id": pit_reference.player_id, "position": pit_reference.position}
            for pit_reference in movement[0]
        ]

        payload = {
            **self._get_game_payload(),
            "movement": plan,
            "captured_stones": movement[1],
        }

        emit("plan_movement", payload)

    def _get_game_payload(self) -> Dict:
        return {
            "game_type": "single",
            "game_state": self.state.name,
            "game_id": self.game.get_game_id(),
            "board": self.game.board.pits,
            "mancalas": self.game.board.mancalas,
            "players": self.players,
            "current_player": self.game.current_player,
        }
