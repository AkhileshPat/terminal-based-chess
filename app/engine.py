import subprocess
import os
from pathlib import Path


class StockfishEngine:
    def __init__(self, engine_path: str | None = None, skill_level: int = 5):
        self.engine_path = engine_path or self._default_engine_path()
        self.skill_level = skill_level
        self.process = subprocess.Popen(
            [self.engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._send("uci")
        self._send("isready")
        self._send(f"setoption name Skill Level value {skill_level}")

    def _default_engine_path(self) -> str:
        base = Path(__file__).resolve().parent.parent
        candidates = [
            base / "Stockfish" / "stockfish-windows-x86-64-avx2.exe",
            base / "Stockfish" / "stockfish-windows-x86-64-avx2" / "stockfish" / "stockfish-windows-x86-64-avx2.exe",
            base / "stockfish-windows-x86-64-avx2.exe",
        ]
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)
        raise FileNotFoundError("Stockfish executable not found. Expected one of: " + ", ".join(str(c) for c in candidates))

    def _send(self, command: str) -> None:
        if self.process.stdin is None:
            raise RuntimeError("Engine process stdin is not available")
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

    def get_best_move(self, fen: str) -> str:
        self._send("position fen " + fen)
        self._send("go depth 8")
        output = []
        while True:
            line = self.process.stdout.readline() if self.process.stdout else ""
            if not line:
                break
            output.append(line.strip())
            if line.startswith("bestmove"):
                return line.split()[1]
        return ""

    def quit(self) -> None:
        self._send("quit")
        if self.process.stdin:
            self.process.stdin.close()
        if self.process.stdout:
            self.process.stdout.close()
        if self.process.stderr:
            self.process.stderr.close()
        self.process.wait(timeout=5)
