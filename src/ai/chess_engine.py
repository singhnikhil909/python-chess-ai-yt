import chess
import chess.engine
import random
import os
from ..utils.constants import STOCKFISH_PATHS, STOCKFISH_SKILL_LEVEL

class ChessEngine:
    def __init__(self):
        self.engine = None
        self.initialize_engine()
        
    def initialize_engine(self):
        """Initialize the chess engine"""
        try:
            # Get the absolute path to the project root
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            print(f"Project root: {project_root}")  # Debug print
            
            # Try to find Stockfish
            stockfish_paths = [
                os.path.join(project_root, "engines", "stockfish.exe"),  # Windows
                os.path.join(project_root, "engines", "stockfish"),      # Linux/Mac
                os.path.join(project_root, "stockfish.exe"),            # Current directory
                os.path.join(project_root, "stockfish")                 # Current directory
            ]
            
            engine_found = False
            for path in stockfish_paths:
                print(f"Trying to load Stockfish from: {path}")
                if os.path.exists(path):
                    print(f"File exists at: {path}")
                    try:
                        self.engine = chess.engine.SimpleEngine.popen_uci(path)
                        engine_found = True
                        print(f"Successfully loaded Stockfish from: {path}")
                        break
                    except Exception as e:
                        print(f"Failed to load Stockfish from {path}: {str(e)}")
                        continue
                else:
                    print(f"File does not exist at: {path}")
            
            if not engine_found:
                print("\nCould not find Stockfish engine. Please ensure it is installed in one of these locations:")
                for path in stockfish_paths:
                    print(f"- {path}")
                print("\nTo fix this:")
                print("1. Download Stockfish from https://stockfishchess.org/download/")
                print("2. Extract the executable")
                print("3. Place it in the 'engines' folder in your project root")
                print("4. Make sure it's named 'stockfish.exe' (Windows) or 'stockfish' (Linux/Mac)")
                print(f"\nCurrent working directory: {os.getcwd()}")
                return
                
            # Configure engine
            self.engine.configure({"Threads": 4, "Hash": 128})
            
        except Exception as e:
            print(f"Error initializing engine: {str(e)}")
            self.engine = None
            
    def get_best_move(self, board, time_limit=1.0):
        """Get the best move from the engine"""
        try:
            if not self.engine:
                print("No engine available, initializing...")
                self.initialize_engine()
                if not self.engine:
                    print("Failed to initialize engine")
                    return None
                    
            # Get the best move
            result = self.engine.play(board, chess.engine.Limit(time=time_limit))
            return result.move
            
        except Exception as e:
            print(f"Error getting best move: {str(e)}")
            # Try to restart the engine
            self.cleanup()
            self.initialize_engine()
            return None
            
    def cleanup(self):
        """Clean up the engine"""
        try:
            if self.engine:
                try:
                    self.engine.quit()
                except Exception as e:
                    print(f"Error during engine quit: {str(e)}")
                finally:
                    self.engine = None
        except Exception as e:
            print(f"Error cleaning up engine: {str(e)}")
            self.engine = None
            
    def __del__(self):
        """Destructor to ensure engine is cleaned up"""
        self.cleanup() 