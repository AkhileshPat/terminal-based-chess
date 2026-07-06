from app.engine import StockfishEngine
from app.game import ChessGame
from app.ui import TerminalUI


def main() -> None:
    ui = TerminalUI()
    game = ChessGame()
    print("Welcome to T-chess")
    rating = input("Enter Stockfish rating (e.g. 800, 1200, 1800): ").strip()
    try:
        strength = int(rating)
    except ValueError:
        strength = 800

    skill = max(1, min(20, (strength // 100) + 1))
    try:
        engine = StockfishEngine(skill_level=skill)
    except FileNotFoundError as exc:
        print(exc)
        print("Please place the Stockfish executable in the project folder or update the engine path.")
        return

    try:
        while not game.is_game_over():
            ui.render(game, show_instruction=(len(game.move_history) == 0))
            move_text = input("Your move: ").strip()
            if move_text.lower() in {"quit", "exit"}:
                break

            ok, message = game.apply_move(move_text)
            if not ok:
                print(message)
                continue

            if game.is_game_over():
                break

            engine_move = engine.get_best_move(game.get_board_fen())
            if not engine_move:
                print("Stockfish did not return a move.")
                break

            ok, engine_san = game.apply_engine_move(engine_move)
            if not ok:
                print(engine_san)
                break
            print(f"Stockfish played: {engine_san}")
    finally:
        engine.quit()

    ui.render(game)
    print("Good Game")


if __name__ == "__main__":
    main()
