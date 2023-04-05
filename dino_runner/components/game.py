from random import randint
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, CLOUD, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.obstacle.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 15
        
        self.x_pos_bg = 0
        self.y_pos_bg = 450
        
        self.x_pos_cloud = SCREEN_WIDTH
        self.y_pos_cloud = 100
        
        self.x_pos_cloudE = SCREEN_WIDTH-500
        self.y_pos_cloudE = 85

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.points = 0

        sound = pygame.mixer.Sound("castlevania.mp3")
        sound.play()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.time.delay(5000)
        pygame.quit()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player)
        self.power_up_manager.update(self.game_speed, self.points, self.player)
        self.points += 1
        if self.player.dino_dead:
            self.playing = False


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_cloud()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)

        if self.player.dino_dead:
            self.player.drawDead(self.screen)

        

        pygame.display.update()        
        pygame.display.flip()


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_cloud(self):
        sw = False
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (image_width +self.x_pos_cloud, self.y_pos_cloud))
        if self.x_pos_cloud <= -image_width:
            self.screen.blit(CLOUD, (image_width +self.x_pos_cloud, self.y_pos_cloud))
            self.x_pos_cloud = SCREEN_WIDTH
        self.draw_cloudE()
        self.x_pos_cloud -= self.game_speed

    def draw_cloudE(self):
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (image_width +self.x_pos_cloudE, self.y_pos_cloudE))
        if self.x_pos_cloudE <= -image_width:
            self.screen.blit(CLOUD, (image_width + self.x_pos_cloudE, self.y_pos_cloudE))
            if randint(0, 1) == 0:
                self.x_pos_cloudE = SCREEN_WIDTH
            else:
                self.x_pos_cloudE = randint(2,3)*SCREEN_WIDTH

        self.x_pos_cloudE -= self.game_speed
        