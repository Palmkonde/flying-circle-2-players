import pygame
import sys
import random


class Game:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)

    DARK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.player1 = self.fetch_data(1)
        self.player2 = self.fetch_data(2)

    def fetch_data(self, player_id: int) -> dict:
        return {
            "id": player_id,
            "position": (random.randint(50, 750), random.randint(50, 550)),
            "direction": random.choice(["Up", "Down", "Left", "Right"]),
            "score": random.randint(0, 100),
        }

    def player_info(self):
        players = [self.player1, self.player2]
        colors = [self.BLUE, self.GREEN]

        for idx, player in enumerate(players):
            position_text = f"Player {player['id']} - Position: {player['position']} | Direction: {player['direction']} | Score: {player['score']}"
            text_surface = self.font.render(position_text, True, colors[idx])
            self.screen.blit(text_surface, (20, 50 * (idx + 1)))

    def main(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.WHITE)

            self.player_info()

            pygame.display.update();
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game_instance = Game()
    game_instance.main()
