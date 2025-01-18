import pygame
import sys
import requests

class Graphic:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.players = self.fetch_player_data()

    def fetch_player_data(self) -> list:
        try:
            response = requests.get('http://yourserver.com/api/players')
            response.raise_for_status()
            data = response.json()
            players_data = data['players']

            if len(players_data) > 10:
                players_data = players_data[:10]

            return [
                {
                    'id': player['id'],
                    'name': player['name'],
                    'color': self.RED if player['id'] % 2 == 1 else self.GREEN,
                    'position': list(player['center']),
                    'velocity': list(player['direction']),
                    'score': player['score'],
                    'radius': 30
                }
                for player in players_data
            ]
        except requests.RequestException as e:
            print(f"Error fetching player data: {e}")
            sys.exit()
        except ValueError as e:
            print(f"JSON decoding error: {e}")
            sys.exit()

    def draw_player(self, player):
        pygame.draw.circle(self.screen, player['color'], (player['position'][0], player['position'][1]), player['radius'])
        text_surface = self.font.render(player['name'], True, self.WHITE)
        text_rect = text_surface.get_rect(center=(player['position'][0], player['position'][1]))
        self.screen.blit(text_surface, text_rect)

    def draw_scoreboard(self):
        players_sorted = sorted(self.players, key=lambda x: x['score'], reverse=True)
        scoreboard_lines = []
        for rank, player in enumerate(players_sorted, start=1):
            scoreboard_lines.append(f"Rank {rank}: {player['name']} - {player['score']}")

        for i, line in enumerate(scoreboard_lines):
            text_surface = self.font.render(line, True, self.BLACK)
            self.screen.blit(text_surface, (self.SCREEN_WIDTH - text_surface.get_width() - 20, 20 + i * 30))

    def update_player_positions(self):
        for player in self.players:
            for i in range(2):
                player['position'][i] += player['velocity'][i]
                if player['position'][i] < player['radius'] or player['position'][i] > (self.SCREEN_WIDTH if i == 0 else self.SCREEN_HEIGHT) - player['radius']:
                    player['velocity'][i] *= -1

    def run_main(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.WHITE)

            self.update_player_positions()

            for player in self.players:
                self.draw_player(player)

            self.draw_scoreboard()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game_instance = Graphic()
    game_instance.run_main()
