import pygame
import time

class GameCharacter:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('images/zombie.png')
        self.image_rect = self.image.get_rect()
        screen_rect = screen.get_rect()
        self.image_rect.center = screen_rect.center
    def show_character(self):
        self.screen.blit(self.image, self.image_rect)
pygame.init()
screen = pygame.display.set_mode((500,500))
screen. fill((255,255,255))

zombie_man = GameCharacter(screen)
zombie_man.show_character()

pygame.display.flip()
time.sleep(5)