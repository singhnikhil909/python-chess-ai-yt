import os

# Window dimensions
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
BOARD_SIZE = 800 # 8 squares * 80px per square

# Square size
SQUARE_SIZE = 80

# Colors
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (247, 247, 105, 128)
VALID_MOVE = (106, 190, 48, 128)
LAST_MOVE = (247, 247, 105, 128)
BUTTON_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Game settings
INITIAL_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Stockfish paths (try different possible locations)
STOCKFISH_PATHS = [
    os.path.join(PROJECT_ROOT, "stockfish", "stockfish-windows-x86-64-avx2.exe"),
    os.path.join(PROJECT_ROOT, "stockfish", "stockfish.exe"),
    os.path.join(PROJECT_ROOT, "stockfish.exe"),
    os.path.join(os.path.dirname(PROJECT_ROOT), "stockfish", "stockfish-windows-x86-64-avx2.exe"),
    os.path.join(os.path.dirname(PROJECT_ROOT), "stockfish", "stockfish.exe"),
    os.path.join(os.path.dirname(PROJECT_ROOT), "stockfish.exe"),
    "stockfish.exe",
    "stockfish"
]

# Leela Chess Zero paths
LCO_PATHS = [
    os.path.join(PROJECT_ROOT, "lc0", "lc0.exe"),
    os.path.join(PROJECT_ROOT, "lc0.exe"),
    os.path.join(os.path.dirname(PROJECT_ROOT), "lc0", "lc0.exe"),
    os.path.join(os.path.dirname(PROJECT_ROOT), "lc0.exe"),
    "lc0.exe",
    "lc0"
]

STOCKFISH_SKILL_LEVEL = 10

# Piece values
PIECE_VALUES = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0
}

# Move types
MOVE_TYPES = {
    'NORMAL': 0,
    'CAPTURE': 1,
    'CASTLE': 2,
    'EN_PASSANT': 3,
    'PROMOTION': 4
}

# Game states
GAME_STATES = {
    'PLAYING': 'playing',
    'CHECKMATE': 'checkmate',
    'STALEMATE': 'stalemate',
    'PAUSED': 'paused'
}

# Stockfish path
STOCKFISH_PATH = "stockfish.exe" 