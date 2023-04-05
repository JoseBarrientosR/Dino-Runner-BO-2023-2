from dino_runner.components.obstacle.cactus import Cactus
from dino_runner.components.obstacle.birds import Birds
from random import randint

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.sw = 0
    
    def update(self, game_speed, player):
        if len(self.obstacles) == 0:
            if randint(0,1) == 1:
                self.obstacles.append(Cactus())
            else:
                self.obstacles.append(Birds(self.sw))
                self.sw = 1 - self.sw

        for obstacle in self.obstacles:
            if obstacle.rect.x < -obstacle.rect.width:
                self.obstacles.pop()
            obstacle.update(game_speed, player)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)