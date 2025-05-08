import pygame
import chess
import sys
from .board import Board
from ..ai.chess_engine import ChessEngine
from ..ui.ui_manager import UIManager
from ..core.event_handler import EventHandler
from ..utils.constants import *

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess AI")
        
        self.board = Board()
        self.engine = ChessEngine()
        self.ui_manager = UIManager(self.screen)
        self.event_handler = EventHandler(self)
        
        self.selected_piece = None
        self.valid_moves = []
        self.current_player = 'white'
        self.game_state = GAME_STATES['PLAYING']
        self.running = True
        self.dragging = False
        self.drag_start = None
        
    def run(self):
        """Main game loop"""
        try:
            while self.running:
                # Handle events
                self.event_handler.handle_events()
                
                # Update game state
                self._update()
                
                # Render
                self._render()
                
                # Update display
                pygame.display.flip()
                
                # Cap the frame rate
                pygame.time.Clock().tick(60)
                
        except Exception as e:
            print(f"Error in game loop: {str(e)}")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'engine'):
                self.engine.cleanup()
            pygame.quit()
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        finally:
            sys.exit()
        
    def _update(self):
        """Update game state"""
        try:
            # Check for game over conditions
            if self.game_state != GAME_STATES['PLAYING']:
                return
                
            # Make AI move if it's black's turn
            if self.current_player == 'black':
                print("Black's turn - making AI move")  # Debug print
                self._make_ai_move()
                
        except Exception as e:
            print(f"Error in update: {str(e)}")
            self.running = False
            
    def _make_ai_move(self):
        """Make a move using the chess engine"""
        try:
            # Convert our board to chess.Board
            chess_board = chess.Board(self.board.get_fen())
            print(f"Current FEN: {chess_board.fen()}")  # Debug print
            
            # Get move from engine
            move = self.engine.get_best_move(chess_board)
            if move:
                # Convert chess move to our format
                # Note: chess.square_rank returns 0-7 from bottom to top
                # and chess.square_file returns 0-7 from left to right
                from_rank = chess.square_rank(move.from_square)
                from_file = chess.square_file(move.from_square)
                to_rank = chess.square_rank(move.to_square)
                to_file = chess.square_file(move.to_square)
                
                # Convert to our coordinate system (0,0 is top-left)
                from_pos = (7 - from_rank, from_file)
                to_pos = (7 - to_rank, to_file)
                
                print(f"Stockfish move: {move}")  # Debug print
                print(f"From square: ({from_rank},{from_file}), To square: ({to_rank},{to_file})")  # Debug print
                print(f"Using coordinates: from {from_pos}, to {to_pos}")  # Debug print
                
                # Verify the piece exists at the from position
                piece = self.board.get_piece_at(from_pos)
                if not piece:
                    print(f"No piece found at {from_pos}")  # Debug print
                    return
                    
                # Verify it's a black piece
                if piece.color != 'black':
                    print(f"Piece at {from_pos} is not black")  # Debug print
                    return
                    
                # Get valid moves for the piece
                valid_moves = self.board.get_valid_moves(piece)
                print(f"Valid moves for piece at {from_pos}: {valid_moves}")  # Debug print
                
                # Make the move
                if self.board.make_move(from_pos, to_pos):
                    self.current_player = 'white'
                    print("AI move successful")  # Debug print
                else:
                    print("AI move failed")  # Debug print
            else:
                print("No AI move returned")  # Debug print
                
        except Exception as e:
            print(f"Error making AI move: {str(e)}")
            self.running = False
                
    def _render(self):
        """Render the game"""
        try:
            # Clear screen
            self.screen.fill((255, 255, 255))
            
            # Render board
            self.ui_manager.render_board(self.board)
            
            # Render pieces
            self.ui_manager.render_pieces(self.board)
            
            # Render valid moves if a piece is selected
            if self.selected_piece:
                self.ui_manager.render_valid_moves(self.valid_moves)
                
            # Render UI elements
            self.ui_manager.render_ui()
            
            # Render dragged piece if dragging
            if self.dragging and self.selected_piece:
                mouse_pos = pygame.mouse.get_pos()
                self.ui_manager.render_dragged_piece(self.selected_piece, mouse_pos)
                
        except Exception as e:
            print(f"Error in render: {str(e)}")
            self.running = False
            
    def handle_piece_selection(self, pos):
        """Handle piece selection"""
        try:
            if self.game_state != GAME_STATES['PLAYING'] or self.current_player != 'white':
                return
                
            # Convert screen position to board coordinates
            row = pos[1] // SQUARE_SIZE
            col = pos[0] // SQUARE_SIZE
            
            # Get piece at position
            piece = self.board.get_piece_at((row, col))
            
            # If a piece is already selected
            if self.selected_piece:
                # If clicking the same piece, deselect it
                if piece == self.selected_piece:
                    self.selected_piece = None
                    self.valid_moves = []
                    self.dragging = False
                    return
                    
                # If clicking a valid move, make the move
                if (row, col) in self.valid_moves:
                    if self.board.make_move(self.selected_piece.position, (row, col)):
                        self.current_player = 'black'
                        
                # Deselect the piece
                self.selected_piece = None
                self.valid_moves = []
                self.dragging = False
                return
                
            # Select the piece if it's the current player's piece
            if piece and piece.color == self.current_player:
                self.selected_piece = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                self.dragging = True
                self.drag_start = (row, col)
        except Exception as e:
            print(f"Error in piece selection: {str(e)}")
            
    def handle_piece_drop(self, pos):
        """Handle piece drop after dragging"""
        try:
            if not self.dragging or not self.selected_piece:
                return
                
            # Convert screen position to board coordinates
            row = pos[1] // SQUARE_SIZE
            col = pos[0] // SQUARE_SIZE
            
            # Check if the drop position is a valid move
            if (row, col) in self.valid_moves:
                if self.board.make_move(self.selected_piece.position, (row, col)):
                    self.current_player = 'black'
                    
            # Reset selection state
            self.selected_piece = None
            self.valid_moves = []
            self.dragging = False
            self.drag_start = None
            
        except Exception as e:
            print(f"Error in piece drop: {str(e)}")
            
    def handle_ui_click(self, pos):
        """Handle UI element clicks"""
        try:
            action = self.ui_manager.handle_click(pos)
            if action == 'new_game':
                self.reset_game()
            elif action == 'undo':
                self.undo_move()
        except Exception as e:
            print(f"Error in UI click: {str(e)}")
            
    def reset_game(self):
        """Reset the game to its initial state"""
        try:
            self.board.reset()
            self.selected_piece = None
            self.valid_moves = []
            self.current_player = 'white'
            self.game_state = GAME_STATES['PLAYING']
            self.dragging = False
            self.drag_start = None
        except Exception as e:
            print(f"Error in reset game: {str(e)}")
            
    def undo_move(self):
        """Undo the last move"""
        try:
            if self.current_player == 'black':
                self.board.undo_move()  # Undo AI move
                self.current_player = 'white'
            if self.current_player == 'white':
                self.board.undo_move()  # Undo player move
                self.current_player = 'black'
        except Exception as e:
            print(f"Error in undo move: {str(e)}")
            
    def show_settings(self):
        """Show settings menu"""
        # TODO: Implement settings menu
        pass 