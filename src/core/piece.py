from ..utils.constants import PIECE_VALUES

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
        self.value = PIECE_VALUES[self.__class__.__name__.lower()]
        
    def get_valid_moves(self, board):
        """Get valid moves for the piece"""
        return []
        
    def move(self, new_position):
        """Move the piece to a new position"""
        self.position = new_position
        self.has_moved = True
        
    def _is_valid_position(self, pos):
        """Check if a position is within the board bounds"""
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8
        
    def _is_same_color_piece(self, board, pos):
        """Check if there's a piece of the same color at the position"""
        piece = board.get_piece_at(pos)
        return piece and piece.color == self.color
        
    def _is_opponent_piece(self, board, pos):
        """Check if there's an opponent's piece at the position"""
        piece = board.get_piece_at(pos)
        return piece and piece.color != self.color
        
    def _get_moves_in_direction(self, board, direction, max_steps=7):
        """Get moves in a given direction until hitting a piece or board edge"""
        moves = []
        current_pos = self.position
        
        for _ in range(max_steps):
            current_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            
            if not self._is_valid_position(current_pos):
                break
                
            if self._is_same_color_piece(board, current_pos):
                break
                
            moves.append(current_pos)
            
            if self._is_opponent_piece(board, current_pos):
                break
                
        return moves
        
    def __str__(self):
        return f"{self.color} {self.__class__.__name__} at {self.position}"
        
class Pawn(Piece):
    def get_valid_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        
        # Forward move
        forward = (self.position[0] + direction, self.position[1])
        if self._is_valid_position(forward) and not board.get_piece_at(forward):
            moves.append(forward)
            
            # Double move from starting position
            if not self.has_moved:
                double_forward = (self.position[0] + 2 * direction, self.position[1])
                if not board.get_piece_at(double_forward):
                    moves.append(double_forward)
                    
        # Captures
        for col_offset in [-1, 1]:
            capture_pos = (self.position[0] + direction, self.position[1] + col_offset)
            if self._is_valid_position(capture_pos) and self._is_opponent_piece(board, capture_pos):
                moves.append(capture_pos)
                
        return moves
        
class Knight(Piece):
    def get_valid_moves(self, board):
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for move in knight_moves:
            new_pos = (self.position[0] + move[0], self.position[1] + move[1])
            if self._is_valid_position(new_pos) and not self._is_same_color_piece(board, new_pos):
                moves.append(new_pos)
                
        return moves
        
class Bishop(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for direction in directions:
            moves.extend(self._get_moves_in_direction(board, direction))
            
        return moves
        
class Rook(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for direction in directions:
            moves.extend(self._get_moves_in_direction(board, direction))
            
        return moves
        
class Queen(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for direction in directions:
            moves.extend(self._get_moves_in_direction(board, direction))
            
        return moves
        
class King(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        # Regular king moves
        for direction in directions:
            new_pos = (self.position[0] + direction[0], self.position[1] + direction[1])
            if self._is_valid_position(new_pos) and not self._is_same_color_piece(board, new_pos):
                moves.append(new_pos)
        
        # Castling moves
        if not self.has_moved:
            # Check kingside castling
            kingside_rook = board.get_piece_at((self.position[0], 7))
            if (isinstance(kingside_rook, Rook) and 
                not kingside_rook.has_moved and 
                not board.get_piece_at((self.position[0], 5)) and 
                not board.get_piece_at((self.position[0], 6)) and
                not board._is_square_attacked((self.position[0], 4), 'black' if self.color == 'white' else 'white') and
                not board._is_square_attacked((self.position[0], 5), 'black' if self.color == 'white' else 'white') and
                not board._is_square_attacked((self.position[0], 6), 'black' if self.color == 'white' else 'white')):
                moves.append((self.position[0], 6))  # Kingside castle
            
            # Check queenside castling
            queenside_rook = board.get_piece_at((self.position[0], 0))
            if (isinstance(queenside_rook, Rook) and 
                not queenside_rook.has_moved and 
                not board.get_piece_at((self.position[0], 1)) and 
                not board.get_piece_at((self.position[0], 2)) and 
                not board.get_piece_at((self.position[0], 3)) and
                not board._is_square_attacked((self.position[0], 2), 'black' if self.color == 'white' else 'white') and
                not board._is_square_attacked((self.position[0], 3), 'black' if self.color == 'white' else 'white') and
                not board._is_square_attacked((self.position[0], 4), 'black' if self.color == 'white' else 'white')):
                moves.append((self.position[0], 2))  # Queenside castle
                
        return moves 