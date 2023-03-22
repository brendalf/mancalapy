from dataclasses import dataclass, field
from typing import List

from .pit import PitReference


@dataclass
class Board:
    num_players: int = field(repr=False)
    num_pits: int = field(repr=False)
    stones: int = field(repr=False)

    pits: List[List[int]] = field(init=False)
    mancalas: List[int] = field(init=False)

    def __post_init__(self) -> None:
        self.pits = [
            [self.stones for _ in range(self.num_pits)] for _ in range(self.num_players)
        ]
        self.mancalas = [0 for _ in range(self.num_players)]

    def get_score(self, player_id: int) -> int:
        return self.mancalas[player_id]

    def get_stones_from_pit(self, pit: PitReference) -> int:
        return self.pits[pit.player_id][pit.position]

    def get_total_stones_in_players_pits(self, player_id: int) -> int:
        return sum(self.pits[player_id])

    def get_oposite_pit_position(self, pit: PitReference) -> int:
        return (pit.position - 5) * -1

    def update_pit(self, pit: PitReference, new_value: int) -> None:
        if new_value < 0:
            raise ValueError("The number stones in a pit can't be negative")

        self.pits[pit.player_id][pit.position] = new_value

    def update_score(self, player_id: int, new_score: int) -> None:
        if new_score < 0:
            raise ValueError("The number of stones in a mancala can't be negative")

        self.mancalas[player_id] = new_score
