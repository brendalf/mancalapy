from unittest import TestCase

from mancala_backend.core.board import Board
from mancala_backend.core.pit import PitReference


class TestBoard(TestCase):
    def setUp(self) -> None:
        self.board = Board(num_players=2, num_pits=6, stones=4)

    def test_post_init(self) -> None:
        pits = [
            [4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4]
        ]
        self.assertEqual(self.board.pits, pits)
        self.assertEqual(self.board.mancalas, [0, 0])

    def test_get_score(self) -> None:
        self.assertEqual(self.board.get_score(0), 0)

    def test_get_stones_from_pit(self) -> None:
        pit = PitReference(player_id=0, position=0)

        self.assertEqual(self.board.get_stones_from_pit(pit), 4)

    def test_get_total_stones_in_players_pits(self) -> None:
        self.assertEqual(self.board.get_total_stones_in_players_pits(0), 24)

    def test_get_opposite_pit_position(self) -> None:
        pits = {
            PitReference(player_id=0, position=0): 5,
            PitReference(player_id=0, position=1): 4,
            PitReference(player_id=0, position=2): 3,
            PitReference(player_id=0, position=3): 2,
            PitReference(player_id=0, position=4): 1,
            PitReference(player_id=0, position=5): 0,
            PitReference(player_id=1, position=0): 5,
            PitReference(player_id=1, position=5): 0,
        }

        for pit, opposite_pit_position in pits.items():
            self.assertEqual(self.board.get_opposite_pit_position(pit), opposite_pit_position)

    def test_update_pit(self) -> None:
        pit0 = PitReference(player_id=0, position=2)
        pit1 = PitReference(player_id=1, position=0)

        self.board.update_pit(pit0, 3)
        self.assertEqual(self.board.get_stones_from_pit(pit0), 3)

        self.board.update_pit(pit0, 2)
        self.assertEqual(self.board.get_stones_from_pit(pit0), 2)

        self.board.update_pit(pit1, 0)
        self.assertEqual(self.board.get_stones_from_pit(pit1), 0)

        with self.assertRaises(ValueError):
            self.board.update_pit(pit1, -2)

    def test_update_score(self) -> None:
        self.board.update_score(0, 3)
        self.assertEqual(self.board.get_score(0), 3)

        self.board.update_score(0, 2)
        self.assertEqual(self.board.get_score(0), 2)

        self.board.update_score(1, 0)
        self.assertEqual(self.board.get_score(1), 0)

        with self.assertRaises(ValueError):
            self.board.update_score(1, -2)

