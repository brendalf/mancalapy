from dataclasses import dataclass, field
from typing import List

from mancala_backend.core.pit import PitReference


@dataclass
class Board:
    """
    This class represents the board of a Mancala game, which consists of a list of pits and a list of mancalas.

    Attributes
    ----------
    num_players : int
        The number of players in the game.
    num_pits : int
        The number of pits per player.
    stones : int
        The number of stones in each pit at the start of the game.
    pits : List[List[int]]
        A list of lists representing the pits on the board.
        Each inner list represents a player's pits, and each entry in the inner list is the number of stones
        in that pit.
    mancalas : List[int]
        A list representing the mancalas on the board. The first entry is the first player's mancala, and the
        second entry is the second player's mancala.
    """

    num_players: int = field(repr=False)
    num_pits: int = field(repr=False)
    stones: int = field(repr=False)

    pits: List[List[int]] = field(init=False)
    mancalas: List[int] = field(init=False)

    def __post_init__(self) -> None:
        """
        Initializes the pits and mancalas lists.
        """
        self.pits = [[self.stones] * self.num_pits for _ in range(self.num_players)]
        self.mancalas = [0] * self.num_players

    def get_score(self, player_id: int) -> int:
        """
        Gets the number of stones in the given player's mancala.

        Parameters
        ----------
        player_id : int
            The ID of the player whose score to get.

        Returns
        -------
        int
            The number of stones in the given player's mancala.
        """
        return self.mancalas[player_id]

    def get_stones_from_pit(self, pit: PitReference) -> int:
        """
        Gets the number of stones in the given pit.

        Parameters
        ----------
        pit : :class:`PitReference`
            The pit to get the number of stones from.

        Returns
        -------
        int
            The number of stones in the given pit.
        """
        return self.pits[pit.player_id][pit.position]

    def get_total_stones_in_players_pits(self, player_id: int) -> int:
        """
        Gets the total number of stones in the given player's pits.

        Parameters
        ----------
        player_id : int
            The ID of the player whose total number of stones to get.

        Returns
        -------
        int
            The total number of stones in the given player's pits.
        """
        return sum(self.pits[player_id])

    def get_opposite_pit_position(self, pit: PitReference) -> int:
        """
        Gets the position of the opposite pit for the given pit.

        Since the pits are positioned in counterclockwise, the opposite pit means the opponent pit that is right before
        the current one. For example, in a game with 6 pits, the opposite pit position for each pit is:
        - pit 0 -> opposite pit 5
        - pit 1 -> opposite pit 4
        - pit 2 -> opposite pit 3
        - pit 3 -> opposite pit 2
        - pit 4 -> opposite pit 1
        - pit 5 -> opposite pit 0

        Parameters
        ----------
        pit : :class:`PitReference`
            A `PitReference` object representing the pit to get the opposite position for.

        Returns
        -------
        int
            An integer representing the position of the opposite pit for the given pit.
        """
        return (pit.position - (self.num_pits - 1)) * -1

    def update_pit(self, pit: PitReference, new_value: int) -> None:
        """
        Updates the number of stones in a pit.

        Parameters
        ----------
        pit : :class:`PitReference`
            A `PitReference` object representing the pit to update.
        new_value : int
            An integer representing the new value to set for the pit.

        Raises
        ------
        ValueError
            If `new_value` is negative.
        """
        if new_value < 0:
            raise ValueError("The number stones in a pit can't be negative")

        self.pits[pit.player_id][pit.position] = new_value

    def update_score(self, player_id: int, new_score: int) -> None:
        """
        Updates the score (number of stones in the mancala) for a player.

        Parameters
        ----------
        player_id : int
            An integer representing the player whose score to update.
        new_score : int
            An integer representing the new score to set for the player.

        Raises
        ------
        ValueError
            If `new_score` is negative.
        """
        if new_score < 0:
            raise ValueError("The number of stones in a mancala can't be negative")

        self.mancalas[player_id] = new_score
