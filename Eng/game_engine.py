"""
It should work independently

Calculating: 
    - Use vector for circle                                                     /
    - When we press a, d something like this vector should move + , - angle     /
    - It should calculate everything
        - Bouncing      /
        - Colliding     /
        - Collecting    /
        - Moving        /
        - Score         /
        - etc.
    
"""
from typing import Tuple
from fix_value import *
import pygame
import random

class Circle:
    """
    Idea:
        [Dual-vectors system]:
            Velocity: affect movement of Circle.
            Head: affect change of Velocity.

    Attributes:
        [Static]:
            self.radius (int): The radius of the circle.
            self.id (int): The ID of the circle (either 1 or 2).

        [Position]:
            self.x (float): The real x-coordinate of the circle in space.
            self.y (float): The real y-coordinate of the circle in space.
            self.x_phantom (int): The displayed x-coordinate (integer part).
            self.y_phantom (int): The displayed y-coordinate (integer part).

        [Movement]:
            self.velocity_vector (list of float): The velocity vector [x, y] that determines how the circle moves.
            self.head_direction_number (int): The direction in degrees (0 to 359) representing the circle's heading.
            self.head_vector (list of float): A unit vector representing the direction of movement, affecting velocity.

    Methods:
        __init__(center: Tuple[float, float], radius: int, id: int):
            Initializes the circle with a given center position, radius, and ID.
        
        steer(shift: int):
            Adjusts the circle's heading by a given shift (in degrees), ensuring the heading stays within [0, 359].

        thrust(magnitude: int):
            Accelerates the circle in the current heading direction by a given magnitude, modifying the velocity vector.

        move():
            Updates the circle's position based on its velocity vector, and updates the phantom position (integer values).

        status():
            Prints a formatted status report showing the circle's ID, position, heading, velocity vector, and speed.

    Example Usage:
    Create a circle at position (0, 0) with a radius of 10 and ID 1
        circle = Circle(center=(0.0, 0.0), radius=10, id=1)

        Steer the circle anticlockwise by 90 degrees
    circle.steer(90)

        Accelerate the circle forward with magnitude 5
    circle.thrust(5)

    Move the circle based on its velocity
        circle.move()

    Print the status of the circle
        circle.status()
    """

    def __init__(self, center: Tuple[float, float], radius: int, id: int) -> None:
        self.x = round(center[0], 5)
        self.y = round(center[1], 5)
        self.x_phantom = int(self.x)
        self.y_phantom = int(self.y)
        self.center = [self.x_phantom, self.y_phantom]
        self.radius = radius 

        # id 
        self.id = id

        # Physics 
        self.velocity_vector = [0, 0]

        self.head_direction_number = 0

        # Assume that player one facing left first
        if id == 1:
            self.head_direction_number = 180
        elif id == 2:
            self.head_direction_number = 0

        self.head_vector = DIRECTIONS[self.head_direction_number]

    def steer(self, shift: int) -> None:
        self.head_direction_number += shift
        if self.head_direction_number < 0:
            self.head_direction_number += 360
        elif self.head_direction_number > 359:
            self.head_direction_number -= 360

        self.head_vector = DIRECTIONS[self.head_direction_number]

    def thrust(self, magnitude: int) -> None:
        self.velocity_vector[0] += self.head_vector[0] * magnitude
        self.velocity_vector[1] += self.head_vector[1] * magnitude
    
    def move(self) -> None:
        self.x = round((self.x + self.velocity_vector[0]), 4)
        self.y = round((self.y + self.velocity_vector[1]), 4)
        self.x_phantom = int(self.x)
        self.y_phantom = int(self.y)
        self.center = [self.x_phantom, self.y_phantom]

    def resist_movement(self, magnitude: float = 0.98, cap: float = 70) -> None:
        velocity = round(get_distance((0,0), self.center), 5)

        if velocity > cap:
            self.velocity_vector[0] *= magnitude
            self.velocity_vector[1] *= magnitude

    def status(self) -> None:
        velocity = round((get_distance((0,0), self.center)), 5)
        print(f"[Cir ID] {str(self.id).ljust(2)},    POS ({str(self.x).ljust(10), str(self.y).ljust(10)}),    DIR {str(self.head_direction_number).ljust(3)},    HEAD {str(self.head_vector).ljust(20)},    VEL ({str(round(self.velocity_vector[0], 4)).ljust(15), str(round(self.velocity_vector[1], 4)).ljust(15)})    |V| {velocity}")

class GameCircle(Circle):
    def __init__(self, center, radius, id):
        super().__init__(center, radius, id)

        self.score = 0
        self.arrow_head = [(self.center[0] + int(self.radius * self.head_vector[1])),
                      (self.center[1] + int(self.radius * self.head_vector[1]))]

    def bounce_edge(self, bound: Tuple[int, int]) -> None:
        if self.x < 0 or self.x > bound[0]:
            self.velocity_vector[0] *= -1
        if self.y < 0 or self.y > bound[1]:
            self.velocity_vector[1] *= -1

    def collision(self, other: Circle) -> None:
        distance = get_distance(self.center, other.center)
        sum_radius = self.radius + other.radius + 3

        if distance < sum_radius:
            self.velocity_vector[0] *= -1
            self.velocity_vector[1] *= -1
            self.move()
            other.velocity_vector[0] *= -1
            other.velocity_vector[1] *= -1
            other.move()

    def control(self, bound: Tuple[int, int], other: Circle,thrust_mod: float = 1, steer_mod: int = 1) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.thrust(thrust_mod)
        if keys[pygame.K_a]:
            self.steer(steer_mod)
        if keys[pygame.K_s]:
            self.thrust(-thrust_mod)
        if keys[pygame.K_d]:
            self.steer(-steer_mod)

        self.status()
        self.move()
        self.resist_movement()
        self.bounce_edge(bound)
        self.collision(other)

        self.arrow_head = [(self.center[0] + int(self.radius * self.head_vector[0])),
                           (self.center[1] + int(self.radius * self.head_vector[1]))]
    
class Medal:
    def __init__(self, center: Tuple[int, int], mid:int, score:int = 1, respawn=True) -> None:
        self.center = center
        
        self.count = 0
        self.alive = True

        self.id = mid
        self.score = score
        self.respawn = respawn

    def get_medal(self, other: Circle, new_center: Tuple[int, int]) -> None:
        distance = round(get_distance(self.center, other.center), 5)
        
        if distance < other.radius:
            if self.respawn:
                self.count += 1
                self.center = new_center
            else:
                self.count = -1
                self.center = [-10, -10]
                self.alive = False
            return self.score
        return 0


class GameEngine:
    def __init__(self, player1: GameCircle, player2: GameCircle, screen: Tuple[int, int] = (800, 600)) -> None:
        self.screen_value = screen
        self.screen = pygame.display.set_mode(screen)
        pygame.display.set_caption("Silly Game")
        self.clock = pygame.time.Clock()
        self.player1 = player1
        self.player2 = player2
        self.medals = []
        for i in range(10):
            self.medals.append(Medal(center=(random.randint(100, 700), random.randint(100, 500)), mid=i))
        self.score_font = pygame.font.SysFont("Arial", 30)

    def draw(self):
        self.screen.fill((0, 0, 0))

        pygame.draw.circle(self.screen, (255, 0, 0), (self.player1.x_phantom, self.player1.y_phantom), self.player1.radius)
        pygame.draw.circle(self.screen, (255, 255, 255), self.player1.arrow_head, 2)
        pygame.draw.circle(self.screen, (0, 255, 0), (self.player2.x_phantom, self.player2.y_phantom), self.player2.radius)
        pygame.draw.circle(self.screen, (255, 255, 255), self.player2.arrow_head, 2)

        for medal in self.medals:
            if medal.alive:
                pygame.draw.circle(self.screen, (255, 255, 0), (medal.center[0], medal.center[1]), 5)

        # Draw scores
        score_text = self.score_font.render(f"Player 1: {self.player1.score}  Player 2: {self.player2.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.screen_value[0] // 2 - score_text.get_width() // 2, 10))

        pygame.display.flip()

    def run(self, fps: int = 60):
        running = True
        while running:
            self.clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player1.control((self.screen_value), self.player2)
            self.player2.control((self.screen_value), self.player1)

            for medal in self.medals:
                if medal.alive:
                    score = medal.get_medal(self.player1, new_center=(random.randint(100, 700), random.randint(100, 500)))
                    if score > 0:
                        self.player1.score += score
                if medal.alive:
                    score = medal.get_medal(self.player2, new_center=(random.randint(100, 700), random.randint(100, 500)))
                    if score > 0:
                        self.player2.score += score

            self.draw()

        pygame.quit()



# Testing area
if __name__ == "__main__":
    pygame.init()

    player1 = GameCircle(center=(300, 300), radius=20, id=1)
    player2 = GameCircle(center=(500, 300), radius=20, id=2)

    engine = GameEngine(player1, player2)

    engine.run()