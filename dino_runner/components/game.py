from random import randint
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, CLOUD, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.obstacle.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components import text_utils

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.playing = False
        self.game_speed = 15   
        self.x_pos_bg = 0
        self.y_pos_bg = 450
        self.x_pos_cloud = SCREEN_WIDTH
        self.y_pos_cloud = 155       
        self.x_pos_cloudE = SCREEN_WIDTH-500
        self.y_pos_cloudE = 200
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.points = 0
        self.death_count = 0


        sound = pygame.mixer.Sound("castlevania.mp3")
        sound.play()

    def run(self):
        # Game loop: events - update - draw
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()
        
        pygame.quit()
    

        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and not self.playing:
                self.playing = True
                self.reset()

   

    def update(self):
        if self.playing:
            user_input = pygame.key.get_pressed()
            self.player.update(user_input)
            self.obstacle_manager.update(self.game_speed, self.player)
            self.power_up_manager.update(self.game_speed, self.points, self.player)
            self.points += 1
            if self.points % 200 == 0:
                self.game_speed += 1
            if self.player.dino_dead:
                self.playing = False
                self.death_count += 1

    def draw(self):
        if self.playing:
            self.clock.tick(FPS)
            self.screen.fill((255, 255, 255))
            self.draw_background()
            self.draw_cloud()
            self.player.draw(self.screen)
            self.draw_score()           
            self.obstacle_manager.draw(self.screen)
            self.power_up_manager.draw(self.screen)     
        else:
            self.draw_menu()  

            

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
        

    def draw_score(self):
        score, score_rect = text_utils.get_message("points " + str(self.points), 20, 1000, 40)
        self.screen.blit(score, score_rect)


    def draw_menu(self):
        white_color = (0, 0, 0)
        self.screen.fill(white_color)
        self.print_menu_element()


    def print_menu_element(self):
        if self.death_count == 0:
            text, text_rect = text_utils.get_message("press any key to star ", 30)
            self.screen.blit(text, text_rect)
        else:
            text, text_rect = text_utils.get_message("press any key to Restar ", 30)
            score, score_rect = text_utils.get_message("you score : " + str(self.points), 30, height=SCREEN_HEIGHT//2 + 50)
            self.screen.blit(text, text_rect)
            self.screen.blit(score, score_rect)
    
    def reset(self):
        self.game_speed = 20
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.points = 0 