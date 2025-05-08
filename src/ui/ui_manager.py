import pygame
import os
from ..utils.constants import *

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        
        # Colors
        self.colors = {
            'light_square': LIGHT_SQUARE,
            'dark_square': DARK_SQUARE,
            'highlight': HIGHLIGHT,
            'valid_move': VALID_MOVE,
            'last_move': LAST_MOVE,
            'white_piece': (255, 255, 255),
            'black_piece': (0, 0, 0),
            'button': BUTTON_COLOR,
            'text': BUTTON_TEXT_COLOR
        }
        
        # Initialize font
        self.font = pygame.font.Font(None, 24)
        
        # UI elements
        self.buttons = {
            'new_game': {
                'rect': pygame.Rect(10, BOARD_SIZE + 10, 100, 30),
                'text': 'New Game'
            },
            'undo': {
                'rect': pygame.Rect(120, BOARD_SIZE + 10, 100, 30),
                'text': 'Undo'
            },
            'settings': {
                'rect': pygame.Rect(230, BOARD_SIZE + 10, 100, 30),
                'text': 'Settings'
            }
        }
        
        # Initialize assets
        self.assets = {}
        self.load_assets()
        
    def load_assets(self):
        """Load game assets"""
        # Load piece images
        piece_dir = os.path.join('assets', 'images', 'imgs-80px')
        piece_mapping = {
            'white_pawn': 'white-pawn.png',
            'white_knight': 'white-knight.png',
            'white_bishop': 'white-bishop.png',
            'white_rook': 'white-rook.png',
            'white_queen': 'white-queen.png',
            'white_king': 'white-king.png',
            'black_pawn': 'black-pawn.png',
            'black_knight': 'black-knight.png',
            'black_bishop': 'black-bishop.png',
            'black_rook': 'black-rook.png',
            'black_queen': 'black-queen.png',
            'black_king': 'black-king.png'
        }
        
        for asset_name, filename in piece_mapping.items():
            path = os.path.join(piece_dir, filename)
            try:
                image = pygame.image.load(path)
                self.assets[asset_name] = image
            except:
                print(f"Warning: Could not load image: {path}")
                # Create a placeholder surface
                surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                color = self.colors['white_piece'] if 'white' in asset_name else self.colors['black_piece']
                pygame.draw.circle(surface, color, 
                                (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//3)
                self.assets[asset_name] = surface
                    
    def render_board(self, board):
        """Render the chess board"""
        try:
            for row in range(8):
                for col in range(8):
                    # Calculate screen position
                    pos_x = col * SQUARE_SIZE
                    pos_y = row * SQUARE_SIZE
                    
                    # Determine square color
                    color = self.colors['light_square'] if (row + col) % 2 == 0 else self.colors['dark_square']
                    
                    # Draw the square
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (pos_x, pos_y, SQUARE_SIZE, SQUARE_SIZE)
                    )
        except Exception as e:
            print(f"Error rendering board: {str(e)}")
            
    def render_pieces(self, board):
        """Render all pieces on the board"""
        try:
            for piece in board.pieces:
                # Skip the piece if it's being dragged
                if hasattr(board, 'selected_piece') and piece == board.selected_piece:
                    continue
                    
                # Get the piece image
                piece_key = f"{piece.color}_{piece.__class__.__name__.lower()}"
                if piece_key in self.assets:
                    # Calculate screen position
                    pos_x = piece.position[1] * SQUARE_SIZE
                    pos_y = piece.position[0] * SQUARE_SIZE
                    
                    # Draw the piece
                    self.screen.blit(self.assets[piece_key], (pos_x, pos_y))
        except Exception as e:
            print(f"Error rendering pieces: {str(e)}")
            
    def render_valid_moves(self, valid_moves):
        """Render valid moves for the selected piece"""
        try:
            for move in valid_moves:
                # Calculate screen position
                pos_x = move[1] * SQUARE_SIZE
                pos_y = move[0] * SQUARE_SIZE
                
                # Draw a circle to indicate valid move
                pygame.draw.circle(
                    self.screen,
                    self.colors['valid_move'],
                    (pos_x + SQUARE_SIZE // 2, pos_y + SQUARE_SIZE // 2),
                    SQUARE_SIZE // 4
                )
        except Exception as e:
            print(f"Error rendering valid moves: {str(e)}")
            
    def render_dragged_piece(self, piece, mouse_pos):
        """Render the piece being dragged"""
        try:
            # Get the piece image
            piece_key = f"{piece.color}_{piece.__class__.__name__.lower()}"
            if piece_key in self.assets:
                # Calculate position to center the piece on the mouse
                piece_size = self.assets[piece_key].get_size()
                pos_x = mouse_pos[0] - piece_size[0] // 2
                pos_y = mouse_pos[1] - piece_size[1] // 2
                
                # Draw the piece at the mouse position
                self.screen.blit(self.assets[piece_key], (pos_x, pos_y))
        except Exception as e:
            print(f"Error rendering dragged piece: {str(e)}")
            
    def render_ui(self):
        """Render UI elements"""
        try:
            # Draw buttons
            for button in self.buttons.values():
                pygame.draw.rect(
                    self.screen,
                    self.colors['button'],
                    button['rect']
                )
                
                # Draw button text
                text = self.font.render(button['text'], True, self.colors['text'])
                text_rect = text.get_rect(center=button['rect'].center)
                self.screen.blit(text, text_rect)
        except Exception as e:
            print(f"Error rendering UI: {str(e)}")
            
    def update(self):
        """Update UI state"""
        # TODO: Add any UI state updates here
        pass
        
    def handle_click(self, pos):
        """Handle click on UI elements"""
        try:
            for action, button in self.buttons.items():
                if button['rect'].collidepoint(pos):
                    return action
            return None
        except Exception as e:
            print(f"Error handling click: {str(e)}")
            return None 