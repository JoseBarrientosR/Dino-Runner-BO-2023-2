import pygame
from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, player): # para actualizar
        self.rect.x -= game_speed
        if self.rect.colliderect(player.dino_rect):
            pygame.time.delay(300)
            player.dino_dead = True


    def draw(self, screen): # para dibujar
        screen.blit(self.image, self.rect)

    