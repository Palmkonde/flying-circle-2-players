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
import random, math, os


class Circle:
    def __init__(self, center: Tuple[float, float], radius: int, id: int, direction: float) -> None:
        # x, y, rad, angle, speed-x speed-y
        
        self.x = center[0]
        self.y = center[1]
        self.radius = radius 

        # id 
        self.id = id

        # Physics 
        self.velocity_vector = [0, 0]
        self.head_vector = [math.cos(direction), math.sin(direction)]

    def steer(self, shift: float = math.pi/180) -> None:
        self.head_vector[0] += math.cos(shift)
        self.head_vector[1] += math.sin(shift)

    def thrust(self, magnitude: int) -> None:
        self.velocity_vector[0] += self.head_vector[0] * magnitude
        self.velocity_vector[1] += self.head_vector[1] * magnitude
    
    def move(self) -> None:
        self.x = self.x + self.velocity_vector[0]
        self.y = self.y + self.velocity_vector[1]

    def resist_movement(self, magnitude: float = 0.98, cap: float = 40) -> None:
        if math.dist((0,0), (self.velocity_vector[0], self.velocity_vector[1])) > cap:
            self.velocity_vector[0] *= magnitude
            self.velocity_vector[1] *= magnitude
            self.move()

    def get_status(self) -> None:
        print("Circle", str(self.id).ljust(3), "Center", str(self.x).ljust(10), str(self.y).ljust(10), "|v|", str(round(math.dist((0,0), self.velocity_vector), 5)).ljust(10), "Direction", math.atan(self.head_vector[1]/self.head_vector[0]))



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

    def control(self, bound: Tuple[int, int], other: Circle, key: Tuple[bool, bool, bool], thrust_mod=1, steer_mod=1) -> None:
        if key[0]:
            self.thrust(thrust_mod)
        if key[1]:
            self.steer(steer_mod)
        if key[2]:
            self.steer(-steer_mod)

        self.move()
        self.resist_movement(magnitude=0.8)
        self.bounce_edge(bound)
        self.collision(other)
        self.get_arrow()

    
class Medal:
    def __init__(self, center: Tuple[int, int], id:int, score:int = 1, respawn=True) -> None:
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
                self.center = new_center
            else:
                self.center = [-10, -10]
                self.alive = False
            return self.score
        return 0

    def get_status(self) -> None:
        print("Coin  ", str(self.id).ljust(3), "Center", str(self.x).ljust(10), str(self.y).ljust(10), "Alive", self.alive)


class GameEngine:
    def __init__(self, player1: PlayerCircle, player2: PlayerCircle, screen: Tuple[int, int] = (800, 600)) -> None:
        self.player1 = player1
        self.player2 = player2
        self.screen = screen

    def run(self, player1key, player2key, medals: int = 10, respawn=True) -> None:
        self.medals_list = list()
        for i in range(medals):
            self.medals_list.append(Medal(center=(random.randint(100, 700), random.randint(100, 500)), id=i, respawn=respawn))

        while True:
            self.player1.control((self.screen), self.player2, player1key)
            self.player2.control((self.screen), self.player1, player2key)

            self.player1.get_status()
            self.player2.get_status()

            for medal in self.medals_list:
                if medal.alive:
                    score = medal.get_medal(self.player1, new_center=(random.randint(100, self.screen[0]-100), random.randint(100, self.screen[1]-100)))
                    self.player1.score += score

                    score = medal.get_medal(self.player2, new_center=(random.randint(100, self.screen[0]-100), random.randint(100, self.screen[1]-100)))
                    self.player2.score += score
                medal.get_status()

            os.system('cls' if os.name == 'nt' else 'clear')
            

if __name__ == "__main__":

    SCREEN = (500, 600)

    player1 = PlayerCircle(center=(200,400), radius=50, id=1, direction=math.pi/2)
    player2 = PlayerCircle(center=(300,400), radius=50, id=2, direction=math.pi/2)

    engine = GameEngine(player1=player1, player2=player2, screen=SCREEN)
    engine.run(player1key=(True, False, True), player2key=(True, True, False))