# Chess AI

A Python-based chess game with AI opponents using Stockfish and Leela Chess Zero engines. This project is a fork of [AlejoG10/python-chess-ai-yt](https://github.com/AlejoG10/python-chess-ai-yt).

## Features

### Implemented
- Interactive chess board with graphical interface
- Support for both Stockfish and Leela Chess Zero engines
- Legal move validation
- Move highlighting and visual feedback
- Support for special moves (castling, en passant, promotion)
- Game state tracking (check, checkmate, stalemate)

### Planned Features
- Opening book integration
- Game analysis mode
- Tournament mode
- Custom engine configuration
- Time controls
- Move history display
- Game statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chess-ai.git
cd chess-ai
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Download chess engines:
   - Download Stockfish from [official website](https://stockfishchess.org/download/)
   - Download Leela Chess Zero from [official website](https://lczero.org/play/download/)
   - Place the engine executables in the `engines` directory

## Usage

1. Run the main game:
```bash
python chess_ai/src/main.py
```

2. Game Controls:
   - Left click to select a piece
   - Left click on a valid square to move
   - Right click to cancel selection
   - Use the menu options for additional features

## Requirements

- Python 3.8 or higher
- Pygame
- Python-chess
- Stockfish or Leela Chess Zero engine

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

This project is a fork of [AlejoG10/python-chess-ai-yt](https://github.com/AlejoG10/python-chess-ai-yt). Special thanks to the original author for the foundation of this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
