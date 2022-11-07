import pygame
import time

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Alien Invasion')
bg_color = (0, 0, 255)
screen.fill(bg_color)
pygame.display.flip()

time.sleep(15)
