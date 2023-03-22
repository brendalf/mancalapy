from dataclasses import dataclass, field
from typing import List, Tuple
from uuid import UUID, uuid4

from .board import Board
from .pit import PitReference


@dataclass()
class MancalaGame:
    board: Board = field(init=False)

    current_player: int = field(default=0, init=False)

    id: UUID = uuid4()

    num_players: int = 2
    num_stones: int = 4
    num_pits: int = 6

    def __post_init__(self) -> None:
        self.board = Board(self.num_players, self.num_stones, self.num_pits)

    def has_game_ended(self) -> bool:
        for player_id in range(self.num_players):
            if self.board.get_total_stones_in_players_pits(player_id) == 0:
                return True

        return False

    def execute_player_movement(self, player_moving: int, selected_pit: int):
        assert (
            player_moving == self.current_player
        ), f"User {player_moving} isn't allowed to move when it's not his turn"

        initial_pit = PitReference(player_id=player_moving, position=selected_pit)

        (
            impacted_pits,
            stones_captured,
            player_moves_again,
        ) = self._calculate_movement_plan(initial_pit)

        self.board.update_pit(initial_pit, 0)

        for impacted_pit in impacted_pits:
            stones = self.board.get_stones_from_pit(impacted_pit) + 1
            self.board.update_pit(impacted_pit, stones)

        if not player_moves_again:
            last_pit = impacted_pits[-1]
            stones_last_pit = self.board.get_stones_from_pit(last_pit)

            # last stone was placed in a empty pit from the player
            if (stones_last_pit == 1) and (last_pit.player_id == player_moving):
                oposite_pit = PitReference(
                    player_id=self._define_next_player(last_pit.player_id),
                    position=self.board.get_oposite_pit_position(last_pit),
                )

                # capture the stone added and all the stones in the opposite pit.
                stones_captured += self.board.get_stones_from_pit(oposite_pit) + 1

                self.board.update_pit(last_pit, 0)
                self.board.update_pit(oposite_pit, 0)

        self.board.update_score(player_moving, stones_captured)

        self.current_player = (
            self.current_player
            if player_moves_again
            else self._define_next_player(self.current_player)
        )

    def _define_next_player(self, current_player_id: int) -> int:
        """
        Defines the next player id to play.
        If the current player is the last player, the next player will be the first player.

        Parameters
        ----------
        current_player_id : int
            The current player id.

        Returns
        -------
        int
            The next player id.
        """
        next_player = current_player_id + 1
        return 0 if next_player == self.num_players else next_player

    def _define_next_pit(self, current_pit: PitReference) -> PitReference:
        """
        Defines the next pit in the board.
        If the current pit is the last pit of a player, the next pit will be first pit of the following player.

        Parameters
        ----------
        current_pit : PitReference
            The reference to the current pit.

        Returns
        -------
        PitReference
            The reference to the next pit.
        """
        next_pit_position = current_pit.position + 1
        next_player = current_pit.player_id

        if next_pit_position >= self.num_pits:
            next_pit_position = 0
            next_player = self._define_next_player(current_pit.player_id)

        return PitReference(player_id=next_player, position=next_pit_position)

    def _calculate_movement_plan(
        self, initial_pit: PitReference
    ) -> Tuple[List[PitReference], int, bool]:
        """
        If the next pit is the mancala of the player who is moving, the stone will be captured.
        """
        stones_to_move = self.board.get_stones_from_pit(initial_pit)

        impacted_pits = []
        stones_captured = 0
        player_moves_again = False

        current_pit = initial_pit

        while stones_to_move > 0:
            next_pit = self._define_next_pit(current_pit)

            # player who is moving hit his mancala
            if (next_pit.position == 0) and (
                current_pit.player_id == initial_pit.player_id
            ):
                stones_captured += 1
                stones_to_move -= 1

                # if there's no stone left, the last place was the player's mancala
                if stones_to_move == 0:
                    player_moves_again = True
                    break

            impacted_pits.append(next_pit)

            stones_to_move -= 1
            current_pit = next_pit

        return impacted_pits, stones_captured, player_moves_again
