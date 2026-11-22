# Online Chess

A two-player chess game built with Python and Pygame. I created this project to learn how a graphical application communicates with a server and to practice representing a real-world game with code.

## Features

- Full 8x8 chess board with black and white piece sprites
- Legal move highlighting
- Turn-based play
- Check and checkmate detection
- Castling
- Pawn double moves and en passant
- Separate white and black player assignments
- Private online rooms using randomly generated room codes
- A WebSocket server that sends moves between players

## What I Learned

Building this project helped me understand object-oriented programming, networking, and game logic. Each chess piece is a class, and the board stores the pieces in tiles. I also learned how to use board snapshots to test whether a move would leave a king in check before allowing the move.

The networking code was especially interesting because it introduced me to asynchronous Python and WebSockets. The server creates a room for the first player, gives that player the white pieces, and waits for a second player to enter the room code and join as black.

## Technologies

- Python
- Pygame Community Edition
- WebSockets
- asyncio
- Pillow
- JSON

## Project Structure

- `main.py` - Starts Pygame and runs the client
- `Board.py` - Creates the board and manages board snapshots
- `Tile.py` - Handles individual squares and moving pieces
- `Piece.py` - Defines each type of chess piece and its movement rules
- `GameObject.py` - Handles mouse input, turns, and game state
- `Client.py` - Connects to the server and sends or receives moves
- `server.py` - Creates rooms and relays moves between players
- `Constants.py` - Stores shared colors and board settings
- `Images/` - Contains the white and black chess piece sprites

## Requirements

- Python 3
- Pygame Community Edition
- `websockets`
- Pillow

## Installation

Clone or download the project, open a terminal in the `Chess` folder, and install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Game

Start the server:

```bash
python server.py
```

The server runs locally on port `9001`.

In a second terminal, start the first player:

```bash
python main.py
```

When prompted, press Enter to create a room. Copy the room code printed by the server.

Then, in another terminal, start the second player:

```bash
python main.py
```

Enter the room code when prompted. The first player will control white pieces, and the second player will control black pieces.

## Controls

- Click a piece to select it
- Gray circles show legal moves
- Click a highlighted square to move the piece
- Press `Escape` to close the game

## Current Limitations

This is a learning project and is designed to run on a local network. It does not currently include player accounts, saved games, timers, or a public matchmaking system.
