from __future__ import annotations

import os
import shutil
from typing import List


class TerminalUI:
    def __init__(self):
        self.width, self.height = shutil.get_terminal_size((100, 40))

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def build_screen(self, game, engine_name: str = "Stockfish", show_instruction: bool = False) -> str:
        self.width, self.height = shutil.get_terminal_size((100, 40))
        board_lines = self._render_board(game)
        move_lines = self._render_moves(game.move_history)
        board_width = max(len(line) for line in board_lines) if board_lines else 24
        left_padding = max(2, (self.width - board_width - 24) // 2)

        lines = [
            "=" * self.width,
            "T-chess".center(self.width),
            "=" * self.width,
            "",
        ]

        center_lines = []
        for idx, line in enumerate(board_lines):
            if idx == 0:
                left_label = "You".center(10)
                right_label = engine_name.center(12)
            elif idx == 1:
                left_label = "Captured: —".center(10)
                right_label = "Captured: —".center(12)
            else:
                left_label = "".center(10)
                right_label = "".center(12)
            center_lines.append(" " * left_padding + left_label + "  " + line + "  " + right_label)

        lines.extend(center_lines)
        lines.extend(["", "Move history:"])
        lines.extend(move_lines)

        if show_instruction:
            lines.append("")
            lines.append("Enter your move in algebraic notation (e.g. e4, Nf3, Qxe5+, O-O).")

        return "\n".join(lines)

    def _render_board(self, game) -> List[str]:
        board_str = game.board.unicode()
        board_lines = [line for line in board_str.splitlines() if line.strip()]
        return [line for line in board_lines]

    def _render_moves(self, moves: List[str]) -> List[str]:
        if not moves:
            return ["  No moves yet"]

        rows = []
        for idx in range(0, len(moves), 2):
            move_number = idx // 2 + 1
            white_move = moves[idx]
            black_move = moves[idx + 1] if idx + 1 < len(moves) else ""
            if black_move:
                rows.append(f"  {move_number}. {white_move:<10} | {black_move}")
            else:
                rows.append(f"  {move_number}. {white_move}")
        return rows

    def render(self, game, engine_name: str = "Stockfish", show_instruction: bool = False) -> None:
        self.width, self.height = shutil.get_terminal_size((100, 40))
        self.clear()
        print(self.build_screen(game, engine_name=engine_name, show_instruction=show_instruction))
