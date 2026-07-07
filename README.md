# T-chess

A simple terminal-based chess app that lets you play against Stockfish from the command line.

## Features
- Starts from a simple command-line prompt
- Accepts a Stockfish strength/rating
- Plays a full game in the terminal
- Displays a basic board and move history
- Prints "Good Game" at the end of a completed match

## Setup
1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

## Notes
- The app uses the bundled Stockfish executable from the workspace.
- Move input uses algebric format such as `e4`.
