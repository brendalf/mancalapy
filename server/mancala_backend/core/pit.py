from dataclasses import dataclass


@dataclass(frozen=True)
class PitReference:
    """
    Represents a reference to a pit on the board of a MancalaGame.

    Attributes
    ----------
    player_id: int
        The player id who owns the pit.
    position : int
        The position of the pit in the player's board.
    """

    player_id: int
    position: int
