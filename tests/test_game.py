import unittest

from app.game import ChessGame


class ChessGameTests(unittest.TestCase):
    def test_accepts_legal_opening_move(self):
        game = ChessGame()
        ok, message = game.apply_move("e4")
        self.assertTrue(ok)
        self.assertEqual(message, "")
        self.assertEqual(game.move_history[-1], "e4")

    def test_rejects_illegal_move(self):
        game = ChessGame()
        ok, message = game.apply_move("e5")
        self.assertFalse(ok)
        self.assertIn("Illegal", message)


if __name__ == "__main__":
    unittest.main()
