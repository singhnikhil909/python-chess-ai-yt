import chess
import chess.engine
import random
import os
from ..utils.constants import STOCKFISH_PATHS, STOCKFISH_SKILL_LEVEL

class StockfishEngine:
    def __init__(self):
        self.engine = None
        self._initialize_engine()
        
    def _initialize_engine(self):
        """Try to initialize Stockfish engine from multiple possible paths"""
        for path in STOCKFISH_PATHS:
            try:
                if os.path.exists(path):
                    self.engine = chess.engine.SimpleEngine.popen_uci(path)
                    self.engine.configure({"Skill Level": STOCKFISH_SKILL_LEVEL})
                    print(f"Successfully loaded Stockfish from: {path}")
                    return
            except Exception as e:
                print(f"Failed to load Stockfish from {path}: {str(e)}")
                continue
                
        print("Warning: Stockfish engine not found. AI moves will be random.")
        self.engine = None
        
    def get_best_move(self, board):
        """Get the best move from Stockfish or a random move if Stockfish is not available"""
        if self.engine:
            try:
                result = self.engine.play(board, chess.engine.Limit(time=0.1))
                return result.move
            except Exception as e:
                print(f"Error getting move from Stockfish: {str(e)}")
                self.engine = None
                
        # If Stockfish is not available or failed, make a random move
        legal_moves = list(board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves)
        return None
        
    def __del__(self):
        """Clean up the engine when the object is destroyed"""
        if self.engine:
            try:
                self.engine.quit()
            except:
                pass 