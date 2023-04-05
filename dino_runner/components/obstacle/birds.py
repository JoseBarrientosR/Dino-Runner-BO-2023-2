from dino_runner.components.obstacle.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

from random import randint

class Birds(Obstacle):
    Y_POS_BIRD = 220
    vec = BIRD
    def __init__(self, type):
        self.type = type
        image = self.vec[self.type]
        super().__init__(image)
        self.rect.y = self.Y_POS_BIRD 