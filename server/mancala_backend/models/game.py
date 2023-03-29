from uuid import uuid4

from mancala_backend.models.player import Player


class Game:
    def __init__(self, player_one: Player, player_two: Player) -> None:
        self.game_id = str(uuid4())
        self.player_one = player_one
        self.player_two = player_two

        self.player_one.set_current_game(self.game_id)
        self.player_two.set_current_game(self.game_id)
