from typing import Tuple, Dict
import random
import math
from pprint import pprint


class Circle:
    def __init__(self, center: Tuple[float, float], radius: int, id: int, direction: float) -> None:
        self.x = center[0]
        self.y = center[1]
        self.radius = radius
        self.id = id
        self.velocity_vector = [0, 0]
        self.head_vector = [math.cos(direction), math.sin(direction)]

    def steer(self, shift: float = math.pi / 180) -> None:
        self.head_vector[0] += math.cos(shift)
        self.head_vector[1] += math.sin(shift)

    def thrust(self, magnitude: int) -> None:
        self.velocity_vector[0] += self.head_vector[0] * magnitude
        self.velocity_vector[1] += self.head_vector[1] * magnitude

    def move(self) -> None:
        self.x += self.velocity_vector[0]
        self.y += self.velocity_vector[1]

    def resist_movement(self, magnitude: float = 0.98, cap: float = 40) -> None:
        speed = math.dist(
            (0, 0), (self.velocity_vector[0], self.velocity_vector[1]))
        if speed > cap:
            self.velocity_vector[0] *= magnitude
            self.velocity_vector[1] *= magnitude
        self.move()

    def get_status(self) -> Dict:
        return {
            'center': (self.x, self.y),
            'direction': (self.head_vector[0], self.head_vector[1]),
            'score': 0  # Placeholder, score will be handled by the PlayerCircle class
        }


class PlayerCircle(Circle):
    def __init__(self, center, radius, id, direction):
        super().__init__(center, radius, id, direction)
        self.score = 0
        self.arrow_head = [self.x + (self.head_vector[0] * self.radius),
                           self.y + (self.head_vector[1] * self.radius)]

    def get_arrow(self):
        self.arrow_head = [self.x + (self.head_vector[0] * self.radius),
                           self.y + (self.head_vector[1] * self.radius)]

    def bounce_edge(self, bound: Tuple[int, int]) -> None:
        if self.x < 0 or self.x > bound[0]:
            self.velocity_vector[0] *= -1
        if self.y < 0 or self.y > bound[1]:
            self.velocity_vector[1] *= -1

    def collision(self, other: Circle) -> None:
        distance = math.dist((self.x, self.y), (other.x, other.y))
        sum_radius = self.radius + other.radius + 3
        if distance < sum_radius:
            self.velocity_vector[0] *= -1
            self.velocity_vector[1] *= -1
            self.move()
            other.velocity_vector[0] *= -1
            other.velocity_vector[1] *= -1
            other.move()

    def control(self, bound: list[int, int], other: Circle, key: Tuple[bool, bool, bool], thrust_mod=1, steer_mod=1) -> None:
        if key[0]:
            self.thrust(thrust_mod)
        if key[1]:
            self.steer(steer_mod)
        if key[2]:
            self.steer(-steer_mod)
        self.move()
        self.resist_movement(magnitude=0.8, cap=100)
        self.bounce_edge(bound)
        self.collision(other)
        self.get_arrow()

    def get_status(self) -> Dict:
        return {
            'center': (self.x, self.y),
            'direction': (self.arrow_head[0], self.arrow_head[1]),
            'score': self.score
        }


class Medal:
    def __init__(self, center: Tuple[int, int], id: int, score: int = 1, respawn=True) -> None:
        self.x = center[0]
        self.y = center[1]
        self.alive = True
        self.id = id
        self.score = score
        self.respawn = respawn

    def get_medal(self, other: Circle, new_center: Tuple[int, int]) -> None:
        distance = math.dist((self.x, self.y), (other.x, other.y))
        if distance < other.radius:
            if self.respawn:
                self.x, self.y = new_center
            else:
                self.x, self.y = [-10, -10]
                self.alive = False
            return self.score
        return 0

    def get_status(self) -> Dict:
        return (self.x, self.y)


class GameEngine:
    def __init__(self, player1: PlayerCircle, player2: PlayerCircle, screen: Tuple[int, int] = (800, 600)) -> None:
        self.player1 = player1
        self.player2 = player2
        self.screen = screen
        self.medals_list = []
        self.state = 0  # Game starts in a waiting state

        self.player1ready, self.player2ready = False, False

    def start_game(self):
        self.state = 1

    def end_game(self):
        self.state = 2

    def run(self, player1key, player2key, medals: int = 10, respawn=True, safe_spawn=100) -> Dict:
        # If both players are in the "Waiting" state and either one of them has given input, start the game
        if self.state == 0:

            if player1key == (True, True, True):
                self.player1ready = True
            if player2key == (True, True, True):
                self.player2ready = True

            # Transition to state 1 if both players are ready
            if self.player1ready and self.player2ready:
                self.start_game()  # Change state to "Playing"
                self.player1ready, self.player2ready = False, False  # Reset readiness state

        elif self.state == 1:
            # Transition to state 2 if either player presses (True, False, True)
            if player1key == (True, False, True) or player2key == (True, False, True):
                self.end_game()

        elif self.state == 2:
            # Transition to state 0 if both players press (True, True, True)
            if player1key == (True, True, True) or player2key == (True, True, True):
                self.state = 0

        # Initialize medals list
        for i in range(medals):
            while True:
                spawn_x = random.randint(100, self.screen[0] - 100)
                spawn_y = random.randint(100, self.screen[1] - 100)
                if math.dist((self.player1.x, self.player1.y), (spawn_x, spawn_y)) > safe_spawn \
                        and math.dist((self.player2.x, self.player2.y), (spawn_x, spawn_y)) > safe_spawn:
                    break
            self.medals_list.append(Medal(center=(random.randint(
                100, 700), random.randint(100, 500)), id=i, respawn=respawn))

        # Process the controls and actions for each player
        self.player1.control(self.screen, self.player2, player1key)
        self.player2.control(self.screen, self.player1, player2key)

        # Handle coin collection
        for medal in self.medals_list:
            if medal.alive:
                # Check for medal collection
                while True:
                    spawn_x = random.randint(100, self.screen[0] - 100)
                    spawn_y = random.randint(100, self.screen[1] - 100)
                    if math.dist((self.player1.x, self.player1.y), (spawn_x, spawn_y)) > safe_spawn \
                            and math.dist((self.player2.x, self.player2.y), (spawn_x, spawn_y)) > safe_spawn:
                        break
                score = medal.get_medal(
                    self.player1, new_center=(spawn_x, spawn_y))
                self.player1.score += score
                score = medal.get_medal(
                    self.player2, new_center=(spawn_x, spawn_y))
                self.player2.score += score

        # Collect current state data to return
        game_state = {
            "state": self.state,
            "coin_position": [medal.get_status() for medal in self.medals_list],
            "players": [
                {
                    "id": 1,
                    "player": self.player1.get_status()
                },
                {
                    "id": 2,
                    "player": self.player2.get_status()
                }
            ]
        }
        return game_state


# Real-time keyboard input handling with pynput (without creating a screen)
def key_apply(client_data: dict) -> Tuple[bool, bool, bool]:
    keys = {
        'w': (True, False, False),
        'a': (False, True, False),
        'd': (False, False, True),
        'space': (True, True, True),
        'GG': (True, False, True)
    }
    if isinstance(client_data, dict):
        key = client_data['key_pressed']
    if isinstance(client_data, str):
        key = client_data

    return keys.get(key, (False, False, False))


# Test key input simulation
if __name__ == "__main__":
    SCREEN = (500, 600)

    player1 = PlayerCircle(center=(200, 400), radius=50,
                           id=1, direction=math.pi / 2)
    player2 = PlayerCircle(center=(300, 400), radius=50,
                           id=2, direction=math.pi / 2)

    engine = GameEngine(player1=player1, player2=player2, screen=SCREEN)

    # Test Input Sequence simulates key presses for player 1 and player 2
    test_input_sequence = [
        ('space', 'w'),    # Player 1: (True, True, True) to start, Player 2: 'w'
        ('w', 'space'),        # Player 1: 'a' (steer left), Player 2: 'd' (steer right)
        ('w', 'a'),        # Player 1: 'w' (thrust), Player 2: 'a' (steer left)
        ('d', 'GG'),       # Player 1: 'd' (steer right), Player 2: 'GG' (game end trigger)
        ('w', 'w'),        # Player 1: 'w' (thrust), Player 2: 'w' (thrust)
        # Player 1: (True, True, True) to restart the game, Player 2: 'a'
        ('space', 'a'),
        ('w', 'd'),        # Player 1: 'w' (thrust), Player 2: 'd' (steer right)
        ('a', 'GG'),       # Player 1: 'a' (steer left), Player 2: 'GG' (game end trigger)
        # Player 1: (True, True, True) to restart the game, Player 2: 'w'
        ('space', 'w')
    ]

    # Simulate key presses and run the game engine
    for player1_key, player2_key in test_input_sequence:
        # Apply keys for both players
        player1key = key_apply(player1_key)
        player2key = key_apply(player2_key)

        # Run the game engine with the current keys
        game_state = engine.run(player1key=player1key, player2key=player2key)

        # Output only the state information
        pprint(game_state)
        # if 'state' in game_state:
        #     print(f"('state': {game_state['state']})")

    # Optionally, print the final scores for verification
    print(f"Player 1 Final Score: {player1.score}")
    print(f"Player 2 Final Score: {player2.score}")

    # client_input = {
    #                 'id': 1,
    #                 'key_pressed': '.'
    #                 }

    # print(key_apply(client_input))
