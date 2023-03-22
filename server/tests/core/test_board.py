from unittest import TestCase

from mancala_backend.core.board import Board


class TestBoard(TestCase):
    def setUp(self) -> None:
        self.board = Board(num_players=2, num_pits=6, stones=4)

    def test_post_init(self):
        pits = [
            [4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4]
        ]
        self.assertEqual(self.board.pits, pits)
        self.assertEqual(self.board.mancalas, [0, 0])

