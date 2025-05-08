import chess
from ..utils.constants import *
from .piece import Pawn, Knight, Bishop, Rook, Queen, King

class Board:
    def __init__(self):
        self.pieces = []
        self.move_history = []
        self.initialize_board()
        
    def initialize_board(self):
        """Initialize the chess board with pieces in their starting positions"""
        # Clear existing pieces
        self.pieces = []
        
        # Initialize pawns
        for col in range(8):
            self.pieces.append(Pawn('white', (6, col)))  # White pawns on row 6
            self.pieces.append(Pawn('black', (1, col)))  # Black pawns on row 1
            
        # Initialize other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(piece_order):
            self.pieces.append(piece_class('white', (7, col)))  # White pieces on row 7
            self.pieces.append(piece_class('black', (0, col)))  # Black pieces on row 0
            
    def get_piece_at(self, position):
        """Get the piece at the given position"""
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None
        
    def get_valid_moves(self, piece):
        """Get valid moves for a piece"""
        if not piece:
            return []
            
        # Get basic valid moves
        moves = piece.get_valid_moves(self)
        
        # Filter out moves that would put/leave the king in check
        valid_moves = []
        for move in moves:
            if not self._would_be_in_check(piece, move):
                valid_moves.append(move)
                
        return valid_moves
        
    def _would_be_in_check(self, piece, move):
        """Check if a move would put or leave the king in check"""
        # Save current state
        original_position = piece.position
        captured_piece = self.get_piece_at(move)
        
        # Make the move
        if captured_piece:
            self.pieces.remove(captured_piece)
        piece.position = move
        
        # Check if king is in check
        king = self._find_king(piece.color)
        in_check = self._is_square_attacked(king.position, 'black' if piece.color == 'white' else 'white')
        
        # Restore state
        piece.position = original_position
        if captured_piece:
            self.pieces.append(captured_piece)
            
        return in_check
        
    def _find_king(self, color):
        """Find the king of the given color"""
        for piece in self.pieces:
            if isinstance(piece, King) and piece.color == color:
                return piece
        return None
        
    def _is_square_attacked(self, square, by_color):
        """Check if a square is attacked by any piece of the given color"""
        for piece in self.pieces:
            if piece.color == by_color:
                if square in piece.get_valid_moves(self):
                    return True
        return False
        
    def make_move(self, from_pos, to_pos):
        """Make a move on the board"""
        try:
            piece = self.get_piece_at(from_pos)
            if not piece:
                print(f"No piece found at {from_pos}")  # Debug print
                return False
                
            # Check if move is valid
            valid_moves = self.get_valid_moves(piece)
            if to_pos not in valid_moves:
                print(f"Invalid move: {to_pos} not in valid moves {valid_moves}")  # Debug print
                return False
                
            # Handle castling
            if isinstance(piece, King):
                # Kingside castle
                if to_pos[1] - from_pos[1] == 2:  # Moving two squares to the right
                    rook_from = (from_pos[0], 7)
                    rook_to = (from_pos[0], 5)
                    rook = self.get_piece_at(rook_from)
                    if rook:
                        rook.move(rook_to)
                        print(f"Kingside castle: Moving rook from {rook_from} to {rook_to}")  # Debug print
                
                # Queenside castle
                elif to_pos[1] - from_pos[1] == -2:  # Moving two squares to the left
                    rook_from = (from_pos[0], 0)
                    rook_to = (from_pos[0], 3)
                    rook = self.get_piece_at(rook_from)
                    if rook:
                        rook.move(rook_to)
                        print(f"Queenside castle: Moving rook from {rook_from} to {rook_to}")  # Debug print
            
            # Capture piece if present
            captured_piece = self.get_piece_at(to_pos)
            if captured_piece:
                print(f"Capturing piece at {to_pos}")  # Debug print
                self.pieces.remove(captured_piece)
                
            # Move the piece
            print(f"Moving piece from {from_pos} to {to_pos}")  # Debug print
            piece.move(to_pos)
            
            # Record the move
            self.move_history.append((from_pos, to_pos, captured_piece))
            
            return True
            
        except Exception as e:
            print(f"Error in make_move: {str(e)}")  # Debug print
            return False
        
    def create_move(self, piece, target):
        """Create a move from a piece to a target position"""
        if target in self.get_valid_moves(piece):
            return (piece, target)
        return None
        
    def undo_move(self):
        """Undo the last move"""
        if not self.move_history:
            return False
            
        from_pos, to_pos, captured_piece = self.move_history.pop()
        piece = self.get_piece_at(to_pos)
        
        # Restore piece position
        piece.position = from_pos
        piece.has_moved = False
        
        # Restore captured piece if any
        if captured_piece:
            self.pieces.append(captured_piece)
            
        return True
        
    def get_fen(self):
        """Get the FEN representation of the board"""
        fen = []
        for row in range(8):
            empty = 0
            row_str = ""
            for col in range(8):
                piece = self.get_piece_at((row, col))
                if piece:
                    if empty > 0:
                        row_str += str(empty)
                        empty = 0
                    piece_char = piece.__class__.__name__[0].lower()
                    if piece.color == 'white':
                        piece_char = piece_char.upper()
                    row_str += piece_char
                else:
                    empty += 1
            if empty > 0:
                row_str += str(empty)
            fen.append(row_str)
            
        # Add the rest of the FEN string
        fen_str = "/".join(fen)
        fen_str += " b "  # Black's turn
        fen_str += "KQkq "  # Castling rights
        fen_str += "- "  # En passant
        fen_str += "0 1"  # Halfmove clock and fullmove number
        
        print(f"Generated FEN: {fen_str}")  # Debug print
        return fen_str
        
    def is_checkmate(self):
        """Check if the current position is checkmate"""
        # Find the current player's king
        king = self._find_king(self.current_player)
        if not king:
            return False
            
        # Check if king is in check
        if not self._is_square_attacked(king.position, 'black' if self.current_player == 'white' else 'white'):
            return False
            
        # Check if any move can get out of check
        for piece in self.pieces:
            if piece.color == self.current_player:
                if self.get_valid_moves(piece):
                    return False
                    
        return True
        
    def is_stalemate(self):
        """Check if the current position is stalemate"""
        # Find the current player's king
        king = self._find_king(self.current_player)
        if not king:
            return False
            
        # Check if king is in check
        if self._is_square_attacked(king.position, 'black' if self.current_player == 'white' else 'white'):
            return False
            
        # Check if any move is possible
        for piece in self.pieces:
            if piece.color == self.current_player:
                if self.get_valid_moves(piece):
                    return False
                    
        return True
        
    def reset(self):
        """Reset the board to its initial state"""
        self.initialize_board()
        self.move_history = [] 