from typing import Tuple, Dict
import pygame
import sys


class Graphics:

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

    def __init__(self, screen: Tuple[int, int], share_data: dict, player_radius=50) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(screen)
        self.data = share_data
        self.clock = pygame.time.Clock()

        self.screen_width = screen[0]
        self.screen_height = screen[1]

        self.font = pygame.font.Font(None, 36)

        self.player_radius = player_radius

    # def populate_players(self, data: dict) -> None:
    #     players_data = data.get("players", [])
    #     print("Players Data:", players_data)

    #     self.players = [
    #         {
    #             "id": player["id"],
    #             "color": self.COLORS[i % len(self.COLORS)],
    #             "position": player.get("center", (0, 0)),
    #             "score": player["score"],
    #             "radius": 50,
    #         }
    #         for i, player in enumerate(players_data)
    #     ]

    def draw_player(self):
        try:
            for player in self.data.get("players"):
                pygame.draw.circle(surface=self.screen, color=self.COLORS[player["id"] - 1],
                                   center=player["player"]["center"], radius=self.player_radius)
                pygame.draw.line(surface=self.screen, color=self.BLACK, width=10,
                                 start_pos=player["player"]["center"], end_pos=player["player"]["direction"])

        # pygame.draw.circle(self.screen, player['color'], (
        #     player['position'][0], player['position'][1]), player['radius'])
        # text_surface = self.font.render(player['name'], True, self.WHITE)
        # text_rect = text_surface.get_rect(
        #     center=(player['position'][0], player['position'][1]))
        # pygame.draw.circle(
        #     self.screen,
        #     player["color"],
        #     (player["position"][0], player["position"][1]),
        #     player["radius"],
        # )
        # text_surface = self.font.render(player["name"], True, self.WHITE)
        # text_rect = text_surface.get_rect(
        #     center=(player["position"][0], player["position"][1])
        # )
        # self.screen.blit(text_surface, text_rect)
        except Exception as e:
            print(f"Error on draw_player: {e}")

    def draw_coin(self):
        try:
            for coin_center in self.data.get("coin_position"):
                pygame.draw.circle(
                    surface=self.screen, color=self.COLORS[4], center=coin_center, radius=5)
        except Exception as e:
            print(f"Error on draw_coin: {e}")

    def draw_scoreboard(self):
        players = self.data.get("players")
        players_sorted = sorted(
            players, key=lambda x: x['player'].get('score', 0), reverse=True)
        scoreboard_lines = []

        for rank, player in enumerate(players_sorted, start=1):
            scoreboard_lines.append(
                f"Rank {rank}: {player['id']} - {player['player']['score']}"
            )

        for i, line in enumerate(scoreboard_lines):
            text_surface = self.font.render(line, True, self.WHITE)
            self.screen.blit(
                text_surface,
                (self.screen_width - text_surface.get_width() - 20, 20 + i * 30),
            )

    def draw_waiting_screen(self):
        # print(f"Data on draw wating screen: {self.data}")
        if self.data.get("state") == 0:
            waiting_font = pygame.font.Font(None, 72)
            waiting_text = waiting_font.render(
                "Waiting for Players", True, self.WHITE)

            controls_text = self.font.render(
                "Press Space Bar to Start", True, self.WHITE)

            waiting_rect = waiting_text.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 - 20)
            )
            controls_rect = controls_text.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 + 40)
            )

            self.screen.blit(waiting_text, waiting_rect)
            self.screen.blit(controls_text, controls_rect)

    def run_graphics(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.BLACK)

            self.draw_waiting_screen()
            self.draw_player()
            self.draw_coin()
            self.draw_scoreboard()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pass
