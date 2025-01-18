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

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

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
        players_sorted = sorted(
            self.players, key=lambda x: x['score'], reverse=True)
    def draw_scoreboard(self, players):
        players_sorted = sorted(players, key=lambda x: x["score"], reverse=True)
        scoreboard_lines = []

        for rank, player in enumerate(players_sorted, start=1):
            scoreboard_lines.append(
                f"Rank {rank}: {player['name']} - {player['score']}")
            scoreboard_lines.append(
                f"{rank}: {player['name']} - {player['score']}"
            )

        for i, line in enumerate(scoreboard_lines):
            text_surface = self.font.render(line, True, self.BLACK)
            self.screen.blit(text_surface, (self.SCREEN_WIDTH -
                             text_surface.get_width() - 20, 20 + i * 30))

    def update_player_positions(self):
        for player in self.players:
            for i in range(2):
                player['position'][i] += player['direction'][i]

                if player['position'][i] < player['radius'] or player['position'][i] > (self.SCREEN_WIDTH if i == 0 else self.SCREEN_HEIGHT) - player['radius']:
                    player['direction'][i] *= -1

            for other_player in self.players:
                if other_player != player:
                    if self.check_collision(player, other_player):
                        self.handle_collision(player, other_player)

    def check_collision(self, player1, player2):
        distance = math.sqrt((player1['position'][0] - player2['position'][0]) ** 2 +
                             (player1['position'][1] - player2['position'][1]) ** 2)
        return distance < (player1['radius'] + player2['radius'])
            self.screen.blit(
                text_surface,
                (self.SCREEN_WIDTH - text_surface.get_width() - 20, 20 + i * 30),
            )

    def update_display(self):
        pygame.display.update()

    def run_graphics(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.WHITE)
            self.update_display()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game_engine = GameEngine()  # ไว้ใส่เกมเอนจิน
    graphics_instance = Graphics()

    example_players_data = [
        {
            "id": i + 1,
            "name": f"Player {i + 1}",
            "color": (255 // (i + 1), 255 // (i + 1), 255),
        }
        for i in range(10)
    ]

    for data in example_players_data:
        game_engine.add_player(data)

    while True:
        game_engine.update_player_positions()

        for player in game_engine.players:
            graphics_instance.draw_player(player)

        graphics_instance.draw_scoreboard(game_engine.players)
        graphics_instance.update_display()
