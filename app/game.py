import chess


class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []

    def apply_move(self, move_text: str) -> tuple[bool, str]:
        move_text = move_text.strip().replace("×", "x")
        try:
            parsed_move = self.board.parse_san(move_text)
        except chess.IllegalMoveError:
            return False, "Illegal move for the current position."
        except (ValueError, chess.InvalidMoveError):
            try:
                parsed_move = chess.Move.from_uci(move_text)
            except ValueError:
                return False, "Invalid move format. Use algebraic notation such as e4, Nf3, Qxe5+, O-O, or O-O-O."

        if parsed_move not in self.board.legal_moves:
            return False, "Illegal move for the current position."

        san_move = self.board.san(parsed_move)
        self.board.push(parsed_move)
        self.move_history.append(san_move)
        return True, ""

    def apply_engine_move(self, uci_text: str) -> tuple[bool, str]:
        try:
            move = chess.Move.from_uci(uci_text)
        except ValueError:
            return False, "Invalid engine move."

        if move not in self.board.legal_moves:
            return False, "Illegal engine move."

        san_move = self.board.san(move)
        self.board.push(move)
        self.move_history.append(san_move)
        return True, san_move

    def is_game_over(self) -> bool:
        return self.board.is_game_over()

    def get_board_fen(self) -> str:
        return self.board.fen()

    def get_side_to_move(self) -> str:
        return "white" if self.board.turn else "black"
