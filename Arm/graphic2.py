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
                pygame.draw.circle(surface=self.screen, color=self.COLORS[3], \
                                center=player["player"]["center"], radius=self.player_radius)
                pygame.draw.line(surface=self.screen, color=self.WHITE, \
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
                pygame.draw.circle(surface=self.screen, color=self.COLORS[4], center=coin_center, radius=5)
        except Exception as e:
            print(f"Error on draw_coin: {e}")


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
                (self.screen_width - text_surface.get_width() - 20, 20 + i * 30),
            )

    def draw_waiting_screen(self):
        print(f"Data on draw wating screen: {self.data}")
        if self.data.get("state") == 0:
            waiting_font = pygame.font.Font(None, 72)
            waiting_text = waiting_font.render("Waiting for Players", True, self.WHITE)

            controls_text = self.font.render("Press Space Bar to Start", True, self.WHITE)

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

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()



if __name__ == "__main__":
    sample_data = {'coin_position': [(153, 149),
                   (467, 409),
                   (109, 392),
                   (567, 402),
                   (138, 107),
                   (348, 357),
                   (625, 368),
                   (195, 107),
                   (238, 240),
                   (437, 360),
                   (599, 353),
                   (171, 128),
                   (134, 160),
                   (254, 165),
                   (466, 280),
                   (606, 247),
                   (193, 103),
                   (595, 316),
                   (400, 420),
                   (247, 212),
                   (552, 499),
                   (455, 477),
                   (350, 345),
                   (128, 189),
                   (458, 337),
                   (381, 154),
                   (186, 154),
                   (387, 131),
                   (476, 310),
                   (350, 326),
                   (569, 148),
                   (270, 134),
                   (372, 114),
                   (363, 225),
                   (104, 422),
                   (269, 195),
                   (242, 143),
                   (111, 255),
                   (182, 232),
                   (581, 474),
                   (165, 241),
                   (462, 387),
                   (224, 144),
                   (597, 136),
                   (268, 330),
                   (400, 127),
                   (114, 221),
                   (681, 291),
                   (539, 215),
                   (499, 197),
                   (224, 227),
                   (614, 423),
                   (210, 166),
                   (526, 321),
                   (666, 454),
                   (570, 234),
                   (197, 263),
                   (257, 206),
                   (544, 260),
                   (223, 307),
                   (538, 179),
                   (375, 226),
                   (131, 284),
                   (246, 206),
                   (131, 284),
                   (161, 195),
                   (462, 468),
                   (591, 309),
                   (501, 120),
                   (223, 350),
                   (564, 373),
                   (313, 176),
                   (464, 293),
                   (525, 329),
                   (424, 123),
                   (500, 230),
                   (444, 334),
                   (628, 173),
                   (459, 154),
                   (691, 242),
                   (467, 401),
                   (214, 286),
                   (163, 379),
                   (661, 244),
                   (242, 485),
                   (307, 327),
                   (614, 139),
                   (413, 157),
                   (178, 408),
                   (615, 164)],
 'players': [{'id': 1,
              'player': {'center': (284.28715971542977, 453.80469636461066),
                         'direction': (489.0617336394547, 499.32910931903433),
                         'score': 3}},
             {'id': 2,
              'player': {'center': (350.7884167516052, 464.4147098480787),
                         'direction': (539.8942238054541, 472.3411606076839),
                         'score': 4}}],
 'state': 0}
    
    graphics_instance = Graphics(screen=(1200, 750),share_data=sample_data)

    graphics_instance.run_graphics()
