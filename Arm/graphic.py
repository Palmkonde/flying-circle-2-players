"""
It should work independently

Graphic:
    - show everything following the data
        - position
        - direction
        - score
        - etc.
"""

import pygame

class Game:

    # Screen
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)

    # Colors
    DARK = (0, 0, 0)

    def __init__(self, player1: dict, player2: dict) -> None:
        self.player1 = player1 
        self.player2 = player2

        # Game setup
        self.screen = pygame.display.set_mode(self.DISPLAY)
        self.clock = pygame.time.CLock()
        
    def run_main(self) -> None:
        """ Main game loop """
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill(self.DARK)

            # Update diplay
            pygame.display.update() 
        pygame.quit()

# testing area
if __name__ == "__main__":
    pass