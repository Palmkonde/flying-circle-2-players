"""
It should work independently

Calculating: 
    - Use vector for circle
    - When we press a, d something like this vector should move + , - angle
    - It should calculate everything
        - Bouncing
        - Colliding 
        - Collecting
        - Moving
        - Score
        - etc.
    
"""
from typing import Tuple

class Circle:
    def __init__(self, center: Tuple[int, int], radius: int, id: int) -> None:
        self.center = center
        self.x = center[0]
        self.y = center[1]
        self.radius = radius 

        # id 
        self.id = id

        # Physics 
        self.velocity_vector = [0, 0] 

        # Assume that player one facing left first
        self.vector = [] # x, y
        if self.id == 1:
            self.vector[0] = (self.x + self.radius) - self.x
            self.vector[1] = self.y
        
        elif self.id == 2:
            self.vector[0] = (self.x - self.radius) - self.x
            self.vector[1] = self.y
        

class GameEngine:
    def __init__(self, player1: Circle, player2: Circle) -> None:
        pass


# Testing area
if __name__ == "__main__":
    pass