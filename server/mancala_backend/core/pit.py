from dataclasses import dataclass


@dataclass(frozen=True)
class PitReference:
    """
    A class representing a reference to a pit on the board.

    Attributes
    ----------
    player_id : int
        The ID of the player who owns the pit.
    position : int
        The position of the pit in the list of pits owned by the player.
    """
    player_id: int
    position: int
