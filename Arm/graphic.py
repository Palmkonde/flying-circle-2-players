import pygame
import sys


class Graphics:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 750
    DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    COLORS = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Purple
        (0, 255, 255),  # Cyan
        (255, 192, 203),  # Pink
        (128, 128, 0),  # Olive
        (0, 128, 128),  # Teal
    ]

    def __init__(self, data: dict) -> None:
        pygame.init()
        
        self.share_data = data
        self.screen = pygame.display.set_mode(self.DISPLAY)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.waiting_font = pygame.font.Font(None, 72)
        self.players = []
        self.waiting_for_players = True

    def fetch_data(self, data: dict) -> None:
        try:
            self.populate_players(data)
            self.waiting_for_players = False
        except ValueError as e:
            print(f"Error processing player data: {e}")
            sys.exit()

    def populate_players(self, data: dict) -> None:
        players_data = data.get("players", [])
        print("Players Data:", players_data)
        
        self.players = [
            {
                "id": player["id"],
                "name": player["name"],
                "color": self.COLORS[i % len(self.COLORS)],
                "position": player.get("center", (0, 0)),
                "score": player["score"],
                "radius": 50,
            }
            for i, player in enumerate(players_data)
        ]



    def draw_player(self, player):
        pygame.draw.circle(self.screen, player['color'], (
            player['position'][0], player['position'][1]), player['radius'])
        text_surface = self.font.render(player['name'], True, self.WHITE)
        text_rect = text_surface.get_rect(
            center=(player['position'][0], player['position'][1]))
        pygame.draw.circle(
            self.screen,
            player["color"],
            (player["position"][0], player["position"][1]),
            player["radius"],
        )
        text_surface = self.font.render(player["name"], True, self.WHITE)
        text_rect = text_surface.get_rect(
            center=(player["position"][0], player["position"][1])
        )
        self.screen.blit(text_surface, text_rect)

    def draw_scoreboard(self):
        players_sorted = sorted(self.players, key=lambda x: x["score"], reverse=True)
        scoreboard_lines = []

        for rank, player in enumerate(players_sorted, start=1):
            scoreboard_lines.append(
                f"Rank {rank}: {player['name']} - {player['score']}"
            )

        for i, line in enumerate(scoreboard_lines):
            text_surface = self.font.render(line, True, self.BLACK)
            self.screen.blit(
                text_surface,
                (self.SCREEN_WIDTH - text_surface.get_width() - 20, 20 + i * 30),
            )

    def draw_waiting_screen(self):
        waiting_text = self.waiting_font.render("Waiting for Players", True, self.BLACK)
        controls_text = self.font.render("Press Space Bar to Start", True, self.BLACK)

        waiting_rect = waiting_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 20)
        )
        controls_rect = controls_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 40)
        )

        self.screen.blit(waiting_text, waiting_rect)
        self.screen.blit(controls_text, controls_rect)

    def run_graphics(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.waiting_for_players = False

            self.screen.fill(self.BLACK)

            if self.waiting_for_players:
                self.draw_waiting_screen()
            else:
                if not self.players:
                    print("No players to draw.")
                for player in self.players:
                    self.draw_player(player)
                self.draw_scoreboard()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()



if __name__ == "__main__":
    graphics_instance = Graphics()

    sample_data = {
        "players": [
            {"id": 1, "name": "Player 1", "score": 100, "center": (100, 100)},
            {"id": 2, "name": "Player 2", "score": 200, "center": (200, 200)},
        ]
    }
    graphics_instance.fetch_data(sample_data)

    graphics_instance.run_graphics()
