import pygame
from ..utils.constants import *

class EventHandler:
    def __init__(self, game_controller):
        self.game_controller = game_controller
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_controller.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if click is on the board
                    if event.pos[0] < BOARD_SIZE and event.pos[1] < BOARD_SIZE:
                        self.game_controller.handle_piece_selection(event.pos)
                    else:
                        self.game_controller.handle_ui_click(event.pos)
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if self.game_controller.dragging:
                        self.game_controller.handle_piece_drop(event.pos)
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_controller.running = False 