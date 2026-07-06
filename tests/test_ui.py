import unittest

from app.game import ChessGame
from app.ui import TerminalUI


class TerminalUITests(unittest.TestCase):
    def test_build_screen_includes_player_labels_and_move_history(self):
        game = ChessGame()
        ui = TerminalUI()
        screen = ui.build_screen(game, engine_name="Stockfish", show_instruction=True)
        self.assertIn("You", screen)
        self.assertIn("Stockfish", screen)
        self.assertIn("Move history", screen)
        self.assertIn("No moves yet", screen)
        self.assertNotIn("Players:", screen)
        self.assertIn("Enter your move in algebraic notation", screen)


if __name__ == "__main__":
    unittest.main()
