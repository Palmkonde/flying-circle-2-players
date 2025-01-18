import pygame
import sys
import requests
import random
import math


class Graphic:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 750
    DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    COLORS = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Purple
        (0, 255, 255),  # Cyan
        (255, 192, 203),  # Pink
        (128, 128, 0),  # Olive
        (0, 128, 128)   # Teal
    ]

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.players = []

    def fetch_data(self) -> None:
        try:
            response = requests.get('http://127.0.0.1:5000/api/players')
            response.raise_for_status()
            data = response.json()
            self.populate_players(data)
        except requests.RequestException as e:
            print(f"Error fetching player data: {e}")
            sys.exit()
        except ValueError as e:
            print(f"JSON decoding error: {e}")
            sys.exit()

    def populate_players(self, data: dict) -> None:
        players_data = data.get('players', [])

        if len(players_data) > len(self.COLORS):
            players_data = players_data[:len(self.COLORS)]

        for i in range(len(players_data)):
            player = players_data[i]
            position = self.generate_unique_position(i)
            self.players.append({
                'id': player['id'],
                'name': player['name'],
                'color': self.COLORS[i % len(self.COLORS)],
                'position': position,
                'score': player['score'],
                'radius': 50,
                'direction': [random.choice([-3, 3]), random.choice([-3, 3])]
            })

    def generate_unique_position(self, index):
        radius = 50
        while True:
            position = [
                random.randint(radius, self.SCREEN_WIDTH - radius),
                random.randint(radius, self.SCREEN_HEIGHT - radius)
            ]
            if not any(self.check_collision({'position': position, 'radius': radius}, player) for player in self.players):
                return position

    def draw_player(self, player):
        pygame.draw.circle(self.screen, player['color'], (
            player['position'][0], player['position'][1]), player['radius'])
        text_surface = self.font.render(player['name'], True, self.WHITE)
        text_rect = text_surface.get_rect(
            center=(player['position'][0], player['position'][1]))
        self.screen.blit(text_surface, text_rect)

    def draw_scoreboard(self):
        players_sorted = sorted(
            self.players, key=lambda x: x['score'], reverse=True)
        scoreboard_lines = []
        for rank, player in enumerate(players_sorted, start=1):
            scoreboard_lines.append(
                f"Rank {rank}: {player['name']} - {player['score']}")

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

    def handle_collision(self, player1, player2):
        temp_direction = list(player1['direction'])
        player1['direction'] = list(player2['direction'])
        player2['direction'] = temp_direction

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
    game_instance = Game()
    
    game_instance.fetch_data()
    
    game_instance.run_main()
