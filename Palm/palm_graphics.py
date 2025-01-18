import pygame
import pygame.display

class Graphic:
    
    SCREEN_WIDTH = 800
    SCREEN_HIGHT = 600
    DISPLAY = (SCREEN_WIDTH, SCREEN_HIGHT)


    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode(self.DISPLAY)
        self.data = {}
        pass
        
    def fetch_data(self, data: dict) -> None:
        self.data = data
    
    def run_graphic(self) -> None:



if __name__ == "__main__":
    pass