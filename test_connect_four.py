"""Unit tests for Connect Four game."""

import unittest
from main import ConnectFour


def debugprint(game, turn=None):
    """Print the board state and optional turn label for debugging."""
    if turn is not None:
        print(f"\nState after turn {turn}:")
    game.print_game_state()

def assert_winner(game, expected_winner):
    """Assert that the expected winner is detected in the current game state."""
    winner = game.winner
    assert winner == expected_winner, f"Expected winner: {expected_winner}, but found: {winner}"

def assert_no_winner(game):
    """Assert that no winner exists yet in the current game state."""
    winner = game.winner
    assert winner == 0, f"Expected no winner, but found player {winner}"


class TestConnectFourInputValidation(unittest.TestCase):
    """Test input validation."""
    
    def setUp(self):
        """Set up a fresh game for each test."""
        self.game = ConnectFour()
    
    def test_valid_move(self):
        """Test that a valid move is accepted."""
        self.assertTrue(self.game.drop_piece(3))
    
    def test_column_too_low(self):
        """Test that a column below 0 is rejected."""
        self.assertFalse(self.game.drop_piece(-1))
        self.assertFalse(self.game.drop_piece(-8))
    
    def test_column_too_high(self):
        """Test that a column >= 7 is rejected."""
        self.assertFalse(self.game.drop_piece(7))
        self.assertFalse(self.game.drop_piece(10))
    
    def test_column_overflow(self):
        """Test that a full column is rejected."""
        # Fill a column
        for _ in range(self.game.rows):
            self.assertTrue(self.game.drop_piece(0))
            assert_no_winner(self.game)
        
        # Next move in that column should fail
        self.assertFalse(self.game.drop_piece(0))


class TestConnectFourHorizontalWin(unittest.TestCase):
    """Test horizontal win detection."""
    
    def test_horizontal_win_player_1(self):
        """Test horizontal win for player 1 with offsets."""
        for offset in range(4):
            with self.subTest(offset=offset):
                self._horizontal_win_with_offset(1, offset)
    
    def test_horizontal_win_player_2(self):
        """Test horizontal win for player 2 with offsets."""
        for offset in range(4):
            with self.subTest(offset=offset):
                self._horizontal_win_with_offset(2, offset)

    
    def _horizontal_win_with_offset(self, winning_player, offset):
        game = ConnectFour()

        if winning_player == 1:
            for col in range(4):
                assert_no_winner(game)
                game.drop_piece(col + offset)
                game.drop_piece(col + offset)
                #debugprint(game, turn=col + 1)
        else:
            start_col = (offset + 4) % game.columns
            for col in range(4):
                assert_no_winner(game)
                game.drop_piece((start_col + col) % game.columns)
                game.drop_piece(col + offset)
                #debugprint(game, turn=col + 1)

        assert_winner(game, winning_player)
    
    def test_no_win_three_in_a_row(self):
        """Test that 3 in a row doesn't count as a win."""
        for offset in range(5):
            with self.subTest(offset=offset):
                self._no_win_three_in_a_row_with_offset(offset)

    def _no_win_three_in_a_row_with_offset(self, offset):
        game = ConnectFour()
        for col in range(3):
            game.drop_piece(col + offset)
            game.drop_piece(col + offset)
            assert_no_winner(game)
            #debugprint(game, turn=col + 1)


class TestConnectFourVerticalWin(unittest.TestCase):
    """Test vertical win detection."""
    
    def setUp(self):
        """Set up a fresh game for each test."""
        self.game = ConnectFour()
    
    def test_vertical_win_player_1(self):
        """Test vertical win for player 1."""
        self.game.drop_piece(0)  # Player 1
        self.game.drop_piece(1)  # Player 2
        assert_no_winner(self.game)
        #debugprint(self.game, turn=1)
        
        self.game.drop_piece(0)  # Player 1
        self.game.drop_piece(1)  # Player 2
        assert_no_winner(self.game)
        #debugprint(self.game, turn=2)
        
        self.game.drop_piece(0)  # Player 1
        self.game.drop_piece(1)  # Player 2
        assert_no_winner(self.game)
        #debugprint(self.game, turn=3)
        
        self.game.drop_piece(0)  # Player 1
        #debugprint(self.game, turn=4)
        
        assert_winner(self.game, 1)
    
    def test_vertical_win_player_2(self):
        """Test vertical win for player 2."""
        for row in range(4):
            assert_no_winner(self.game)
            self.game.drop_piece(1 + (row * 2) % 5)  # Player 1
            self.game.drop_piece(0)  # Player 2
            #debugprint(self.game, turn=row + 1)
        
        assert_winner(self.game, 2)
    
    def test_no_win_three_vertical(self):
        """Test that 3 vertical pieces don't count as a win."""
        for _ in range(3):
            self.game.drop_piece(0)
            self.game.drop_piece(1)
            assert_no_winner(self.game)
            #debugprint(self.game)


class TestConnectFourDiagonalNWSEWin(unittest.TestCase):
    """Test diagonal NW-SE (top-left to bottom-right) win detection."""
    
    def _play_diagonal_nwse_win_player_1(self, offset=0):
        game = ConnectFour()
        player_1_cols = [3, 2, 0, 1, 3, 0]
        player_2_cols = [2, 1, 1, 0, 0]

        for idx in range(len(player_2_cols)):
            assert_no_winner(game)
            game.drop_piece(player_1_cols[idx] + offset)
            game.drop_piece(player_2_cols[idx] + offset)
            #debugprint(game, turn=idx + 1)

        game.drop_piece(player_1_cols[-1] + offset)
        #debugprint(game)
        assert_winner(game, 1)

    def _play_diagonal_nwse_win_player_2(self, offset=0):
        game = ConnectFour()
        player_1_cols = [2, 1, 1, 0, 0]
        player_2_cols = [3, 2, 1, 0, 0]

        for idx in range(len(player_2_cols)):
            assert_no_winner(game)
            game.drop_piece(player_1_cols[idx] + offset)
            game.drop_piece(player_2_cols[idx] + offset)
            #debugprint(game, turn=idx + 1)

        assert_winner(game, 2)

    def test_diagonal_nwse_win_player_1(self):
        """Test diagonal NW-SE win for player 1 with offsets."""
        for offset in range(4):
            with self.subTest(offset=offset):
                self._play_diagonal_nwse_win_player_1(offset)

    def test_diagonal_nwse_win_player_2(self):
        """Test diagonal NW-SE win for player 2 with offsets."""
        for offset in range(4):
            with self.subTest(offset=offset):
                self._play_diagonal_nwse_win_player_2(offset)


class TestConnectFourDiagonalSWNEWin(unittest.TestCase):
    """Test diagonal SW-NE (bottom-left to top-right) win detection."""
    
    def setUp(self):
        """Set up a fresh game for each test."""
        self.game = ConnectFour()

    def _play_diagonal_swne_win_player_1(self, offset=0):
        game = ConnectFour()
        player_1_cols = [0, 1, 3, 2, 3, 3]
        player_2_cols = [1, 2, 2, 3, 0]

        for idx in range(len(player_2_cols)):
            assert_no_winner(game)
            col = player_1_cols[idx] + offset
            game.drop_piece(col)
            col = player_2_cols[idx] + offset
            game.drop_piece(col)
            #debugprint(game, turn=idx + 1)

        game.drop_piece(player_1_cols[-1] + offset)
        #debugprint(game)

        assert_winner(game, 1)

    def _play_diagonal_swne_win_player_2(self, offset=0):
        game = ConnectFour()
        player_1_cols = [1, 2, 2, 3, 3]
        player_2_cols = [0, 1, 2, 3, 3]

        for idx in range(len(player_2_cols)):
            assert_no_winner(game)
            game.drop_piece(player_1_cols[idx] + offset)
            game.drop_piece(player_2_cols[idx] + offset)
            #debugprint(game, turn=idx + 1)

        assert_winner(game, 2)

    def test_diagonal_swne_win_player_1(self):
        """Test diagonal SW-NE win for player 1 with offsets."""
        for offset in range(4):
            with self.subTest(offset=offset):
                self._play_diagonal_swne_win_player_1(offset)

    def test_diagonal_swne_win_player_2(self):
        """Test diagonal SW-NE win for player 2 with offsets."""
        for offset in range(4):
            with self.subTest(offset=offset):
                self._play_diagonal_swne_win_player_2(offset)



class TestConnectFourGameState(unittest.TestCase):
    """Test game state retrieval."""
    
    def setUp(self):
        """Set up a fresh game for each test."""
        self.game = ConnectFour()

    def test_new_game_state_does_not_have_winner(self):
        """Test that a new game state does not have a winner."""
        assert_no_winner(self.game)
    
    def test_get_game_state_returns_matrix(self):
        """Test that get_game_state returns the correct matrix."""
        state = self.game.get_game_state()
        self.assertEqual(len(state), self.game.rows)
        self.assertEqual(len(state[0]), self.game.columns)
    
    def test_get_game_state_initial_empty(self):
        """Test that initial game state is all zeros."""
        state = self.game.get_game_state()
        for row in state:
            for cell in row:
                self.assertEqual(cell, 0)
    
    def test_get_game_state_reflects_moves(self):
        """Test that game state reflects pieces played."""
        self.game.drop_piece(0)
        state = self.game.get_game_state()
        # Piece should be at bottom of column 0 (row 0)
        self.assertEqual(state[0][0], 1)
    
    def test_get_game_state_is_copy(self):
        """Test that returned state is a copy, not a reference."""
        state1 = self.game.get_game_state()
        state1[0][0] = 99
        state2 = self.game.get_game_state()
        # Original board should not be affected
        self.assertEqual(state2[0][0], 0)


if __name__ == "__main__":
    unittest.main()
