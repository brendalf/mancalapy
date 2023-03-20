from collections import namedtuple
from typing import List, Tuple
from uuid import UUID, uuid4
from dataclasses import dataclass, field


PitPointer = namedtuple("Pit", ["player", "pit"])

@dataclass
class MancalaGame():
    current_player: int

    id: UUID = uuid4()
    players: int = 2
    board: List[List[int]] = field(default_factory=list)

    stones: int = 4 
    pits: int = 6

    def __init__(self) -> None:
        super()

        self.current_player = 0
        self.board = [
            [self.stones for _ in range(self.pits)]
            for _ in range(self.players)
        ]
        self.mancalas = [0 for _ in range(self.players)]

        print(self.board)

    def get_player_pits(self, player) -> List[int]:
        return self.board[player]

    def has_game_ended(self) -> bool:
        for player_board in self.board:
            if sum(player_board) == 0:
                return True

        return False

    def define_next_player(self, current_player: int) -> int:
        next_player = current_player + 1
        return 0 if next_player == self.players else next_player

    def define_next_pit(self, current_pit: PitPointer, player_moving: int) -> Tuple[PitPointer, bool]:
        next_pit = current_pit.pit + 1
        next_player = current_pit.player
        collected_stone = False
        
        if next_pit >= self.pits:
            if current_pit.player == player_moving:
                collected_stone = True

            next_pit = 0
            next_player = self.define_next_player(current_pit.player)

        return PitPointer(player=next_player, pit=next_pit), collected_stone

    def define_movement_impact(self, player_moving: int, selected_pit: int) -> Tuple[List[PitPointer], int]:
        stones_to_move = self.get_player_pits(player_moving)[selected_pit]
        stones_captured = 0

        impacted_pits = []

        current_pit = PitPointer(player=player_moving, pit=selected_pit)

        while stones_to_move > 0:
            next_pit, collected_stone = self.define_next_pit(current_pit, player_moving)

            if collected_stone:
                stones_captured += 1
                stones_to_move -= 1

            impacted_pits.append(next_pit)

            stones_to_move -= 1
            current_pit = next_pit

        return impacted_pits, stones_captured

    def execute_player_movement(self, player_moving: int, selected_pit: int):
        assert player_moving == self.current_player, f"User {player_moving} isn't allowed to move when it's not his turn"
        
        impacted_pits, stones_captured = self.define_movement_impact(player_moving, selected_pit)
        self.mancalas[player_moving] += stones_captured

        for impacted_pit in impacted_pits:
            self.board[impacted_pit.player][impacted_pit.pit] += 1

        # TODO: only if last pit is the mancala or the a empty pit
        self.current_player = self.define_next_player(self.current_player)
        
