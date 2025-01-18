import pygame
import sys
import requests


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

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.players = []

    def fetch_data(self) -> None:
        try:
            response = requests.get("http://127.0.0.1:5000/api/players")
            response.raise_for_status()
            data = response.json()
            self.populate_players(data)
            print("Player data fetched successfully.")
            for player in self.players:
                print(
                    f"ID: {player['id']}, Position: {player['position']}, Direction: {player['direction']}, Score: {player['score']}"
                )

        except requests.RequestException as e:
            print(f"Error fetching player data: {e}")
            sys.exit()
        except ValueError as e:
            print(f"JSON decoding error: {e}")
            sys.exit()

    def populate_players(self, data: dict) -> None:
        players_data = data.get("players", [])

        if len(players_data) > len(self.COLORS):
            players_data = players_data[: len(self.COLORS)]

        self.players = [
            {
                "id": player["id"],
                "name": player["name"],
                "color": self.COLORS[i % len(self.COLORS)],
                "position": player["center"],
                "score": player["score"],
                "radius": 50,
                "direction": player.get("direction"),
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

        for rank, player in enumerate(players_sorted):
            scoreboard_text = f"Rank {rank + 1}: {player['name']} - {player['score']}"
            text_surface = self.font.render(scoreboard_text, True, self.BLACK)
            self.screen.blit(
                text_surface,
                (self.SCREEN_WIDTH - text_surface.get_width() - 20, 20 + rank * 30),
            )

    def run_graphics(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.BLACK)

            for player in self.players:
                self.draw_player(player)

            self.draw_scoreboard()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    graphics_instance = Graphics()

    graphics_instance.fetch_data()

    graphics_instance.run_graphics()
