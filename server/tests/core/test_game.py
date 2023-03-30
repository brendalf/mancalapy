import unittest

from mancala_backend.core.game import MancalaGame
from mancala_backend.core.pit import PitReference


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = MancalaGame()

    def test_has_game_ended(self) -> None:
        self.assertFalse(self.game.has_game_ended())

        self.game.board.update_pit(PitReference(0, 0), 0)
        self.game.board.update_pit(PitReference(0, 1), 0)
        self.game.board.update_pit(PitReference(0, 2), 0)
        self.game.board.update_pit(PitReference(0, 3), 0)
        self.game.board.update_pit(PitReference(0, 4), 0)
        self.game.board.update_pit(PitReference(0, 5), 0)

        self.assertTrue(self.game.has_game_ended())

    def test_wrong_player_cannot_play(self) -> None:
        self.game.current_player = 0

        with self.assertRaises(PermissionError):
            self.game.execute_player_movement(player_moving=1, selected_pit=2)

    def test_execute_player_movement(self) -> None:
        # last stone on mancala, player 0 moves again
        self.game.execute_player_movement(player_moving=0, selected_pit=2)
        self.assertEqual(self.game.current_player, 0)
        self.assertEqual(self.game.board.pits, [[4, 4, 0, 5, 5, 5], [4, 4, 4, 4, 4, 4]])
        self.assertEqual(self.game.board.mancalas, [1, 0])

        # player 0 distribute stones in player 1 pits
        self.game.execute_player_movement(player_moving=0, selected_pit=4)
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(self.game.board.pits, [[4, 4, 0, 5, 0, 6], [5, 5, 5, 4, 4, 4]])
        self.assertEqual(self.game.board.mancalas, [2, 0])

        # last stone on mancala, player 1 moves again
        self.game.execute_player_movement(player_moving=1, selected_pit=1)
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(self.game.board.pits, [[4, 4, 0, 5, 0, 6], [5, 0, 6, 5, 5, 5]])
        self.assertEqual(self.game.board.mancalas, [2, 1])

        # player 1 distribute stones
        self.game.execute_player_movement(player_moving=1, selected_pit=0)
        self.assertEqual(self.game.current_player, 0)
        self.assertEqual(self.game.board.pits, [[4, 4, 0, 5, 0, 6], [0, 1, 7, 6, 6, 6]])
        self.assertEqual(self.game.board.mancalas, [2, 1])

        # last stone hit an empty mancala, player 0 capture all stones in the opponent oposite pit
        self.game.execute_player_movement(player_moving=0, selected_pit=0)
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(self.game.board.pits, [[0, 5, 1, 6, 0, 6], [0, 0, 7, 6, 6, 6]])
        self.assertEqual(self.game.board.mancalas, [4, 1])

    def test_wrong_player_id_cannot_play(self) -> None:
        with self.assertRaises(ValueError):
            self.game.execute_player_movement(-1, 0)
            self.game.execute_player_movement(3, 0)

    def test_define_next_player(self) -> None:
        self.game.current_player = 0

        self.assertEqual(self.game._define_next_player(0), 1)
        self.assertEqual(self.game._define_next_player(1), 0)

        self.game_with_three_players = MancalaGame(num_players=3)
        self.game_with_three_players.current_player = 0

        self.assertEqual(self.game_with_three_players._define_next_player(0), 1)
        self.assertEqual(self.game_with_three_players._define_next_player(1), 2)
        self.assertEqual(self.game_with_three_players._define_next_player(2), 0)

    def test_define_next_pit(self) -> None:
        pits = [
            (PitReference(player_id=0, position=0), PitReference(player_id=0, position=1)),
            (PitReference(player_id=0, position=1), PitReference(player_id=0, position=2)),
            (PitReference(player_id=0, position=2), PitReference(player_id=0, position=3)),
            (PitReference(player_id=0, position=3), PitReference(player_id=0, position=4)),
            (PitReference(player_id=0, position=4), PitReference(player_id=0, position=5)),
            (PitReference(player_id=0, position=5), PitReference(player_id=1, position=0)),
            (PitReference(player_id=1, position=0), PitReference(player_id=1, position=1)),
            (PitReference(player_id=1, position=2), PitReference(player_id=1, position=3)),
            (PitReference(player_id=1, position=4), PitReference(player_id=1, position=5)),
            (PitReference(player_id=1, position=5), PitReference(player_id=0, position=0)),
        ]

        for current_pit, next_pit in pits:
            self.assertEqual(self.game._define_next_pit(current_pit), next_pit)

    def test_calculate_movement_plan(self) -> None:
        initial_pit = PitReference(player_id=0, position=2)
        impacted_pits, stones_captured, player_moves_again = self.game.calculate_movement_plan(initial_pit)
        
        self.assertEqual(impacted_pits, [PitReference(0, 3), PitReference(0, 4), PitReference(0, 5)])
        self.assertEqual(stones_captured, 1)
        self.assertTrue(player_moves_again)

        self.game.execute_player_movement(0, 2)

        initial_pit = PitReference(player_id=0, position=3)
        impacted_pits, stones_captured, player_moves_again = self.game.calculate_movement_plan(initial_pit)

        self.assertEqual(impacted_pits, [PitReference(0, 4), PitReference(0, 5), PitReference(1, 0), PitReference(1, 1)])
        self.assertEqual(stones_captured, 1)
        self.assertFalse(player_moves_again)

        self.game.execute_player_movement(0, 3)

        initial_pit = PitReference(player_id=1, position=4)
        impacted_pits, stones_captured, player_moves_again = self.game.calculate_movement_plan(initial_pit)

        self.assertEqual(impacted_pits, [PitReference(1, 5), PitReference(0, 0), PitReference(0, 1)])
        self.assertEqual(stones_captured, 1)
        self.assertFalse(player_moves_again)

if __name__ == '__main__':
    unittest.main()
