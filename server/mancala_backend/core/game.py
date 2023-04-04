from dataclasses import dataclass, field
from typing import List, Tuple
from uuid import UUID, uuid4

from mancala_backend.core.board import Board
from mancala_backend.core.pit import PitReference


@dataclass()
class MancalaGame:
    """
    A class representing a Mancala game.

    Attributes
    ----------
    board : :class:`Board`
        The board where the game is being played.
    current_player : int
        The player who should move next.
    id : :class:`UUID`
        The unique identifier for the game.
    num_players : int
        The number of players in the game.
    stones_per_pit : int
        The number of stones that each pit should have at the beginning of the game.
    pits_per_player : int
        The number of pits that each player should have at the beginning of the game.
    """

    board: Board = field(init=False)

    current_player: int = field(default=0, init=False)

    id: UUID = uuid4()

    num_players: int = 2
    stones_per_pit: int = 4
    pits_per_player: int = 6

    def __post_init__(self) -> None:
        self.board = Board(self.num_players, self.pits_per_player, self.stones_per_pit)

    def has_game_ended(self) -> bool:
        """
        Checks if the game has ended.

        The game ends when a player can't move anymore.
        In other words, when all the pits of a player are empty.

        Returns
        -------
        bool
            A boolean indicating if the game has ended.
        """
        for player_id in range(self.num_players):
            if self.board.get_total_stones_in_players_pits(player_id) == 0:
                return True

        return False

    def finish(self) -> None:
        """
        Finish game, moving stones still available in pits to the scores.
        """
        for player_id in range(self.num_players):
            stones = self.board.get_total_stones_in_players_pits(player_id)

            if stones > 0:
                score = self.board.get_score(player_id) + stones
                self.board.update_score(player_id, score)

            self.board.zero_stones_in_pits(player_id)

    def get_winner(self) -> int:
        """
        Gets the player id of the winner who won the match.
        """
        if not self.has_game_ended():
            raise ValueError("Game is still running. No winner defined.")

        max_score = max(self.board.mancalas)
        return self.board.mancalas.index(max_score)

    def execute_player_movement(self, player_moving: int, selected_pit: int) -> None:
        """
        Executes a player movement.

        A movement is executed like this:
        - The player will move all stones from the selected pit to the following pits.
        - If the last stone is placed in the player's mancala, the player will receive an extra move.
        - If the last stone is placed in a empty pit from the player, the player will capture the stone added and all the stones in the opposite pit.

        Parameters
        ----------
        player_moving : int
            The player id who is moving the stones.
        selected_pit : int
            The position of the pit where the player is moving the stones from.

        Raises
        ------
        ValueError
            If the player id isn't valid.
        PermissionError
            If the player id isn't the current player.
        """
        # validate inputs
        if player_moving not in range(self.num_players):
            raise ValueError(
                f"The player id {player_moving} isn't valid. It needs to be one of the following values: {list(range(self.num_players))}"
            )

        if player_moving != self.current_player:
            raise PermissionError(
                f"User {player_moving} isn't allowed to move when it's not his turn"
            )

        initial_pit = PitReference(player_id=player_moving, position=selected_pit)

        movement_plan = self.calculate_movement_plan(initial_pit)
        impacted_pits, stones_captured, player_moves_again = movement_plan

        self.board.update_pit(initial_pit, 0)

        for impacted_pit in impacted_pits:
            stones = self.board.get_stones_from_pit(impacted_pit) + 1
            self.board.update_pit(impacted_pit, stones)

        if not player_moves_again:
            last_pit = impacted_pits[-1]
            stones_last_pit = self.board.get_stones_from_pit(last_pit)

            oposite_pit = PitReference(
                player_id=self._define_next_player(last_pit.player_id),
                position=self.board.get_opposite_pit_position(last_pit),
            )

            # last stone was placed in a empty pit from the player
            if (
                (stones_last_pit == 1)
                and (self.board.get_stones_from_pit(oposite_pit) > 0)
                and (last_pit.player_id == player_moving)
            ):
                # capture the stone added and all the stones in the opposite pit.
                stones_captured += self.board.get_stones_from_pit(oposite_pit) + 1

                self.board.update_pit(last_pit, 0)
                self.board.update_pit(oposite_pit, 0)

        current_stones = self.board.get_score(player_id=player_moving)
        self.board.update_score(player_moving, current_stones + stones_captured)

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
        return (current_player_id + 1) % self.num_players

    def _define_next_pit(self, current_pit: PitReference) -> PitReference:
        """
        Defines the next pit in the board.
        If the current pit is the last pit of a player, the next pit will be first pit of the following player.

        Parameters
        ----------
        current_pit : :class:`PitReference`
            The reference to the current pit.

        Returns
        -------
        PitReference
            The reference to the next pit.
        """
        next_pit = (current_pit.position + 1) % self.pits_per_player
        next_player = (
            self._define_next_player(current_pit.player_id)
            if next_pit < current_pit.position
            else current_pit.player_id
        )

        return PitReference(player_id=next_player, position=next_pit)

    def calculate_movement_plan(
        self, initial_pit: PitReference
    ) -> Tuple[List[PitReference], int, bool]:
        """
        Calculates the movement plan based on a initial pit.
        If the last stone is placed in the player's mancala, the player will receive an extra move.

        Parameters
        ----------
        initial_pit : :class:`PitReference`
            The reference to the pit where the player is moving the stones from.

        Returns
        -------
        Tuple[List[PitReference], int, bool]
            A tuple with the following elements:
            - A list of the impacted pits.
            - The number of stones captured.
            - A boolean indicating if the player who is moving received an extra move.
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

    def get_game_id(self) -> str:
        """Returns the game id as string."""
        return self.id.hex
