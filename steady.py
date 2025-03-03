import pygame
from pygame.sprite import Sprite
import sys

class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)
        self.raindrop_speed = .5
class Raindrop(Sprite):
    def __init__(self, rd_game):
        super().__init__()
        self.screen = rd_game.screen
        self.settings = rd_game.settings
        self.image = pygame.image.load('images/raindrop.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.y = float(self.rect.y)
    def check_disappeared(self):
        if self.rect.top > self.screen.get_rect().bottom:
            return True
        else:
            return False
    def update(self):
        self.y += self.settings.raindrop_speed
        self.rect.y = self.y


class RaindropsGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Raindrops")
        self.raindrops = pygame.sprite.Group()
        self._create_drops()

    def run_game(self):
        while True:
            self._check_events()
            self._update_raindrops()
            self._update_screen()
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
    def _create_drops(self):
        drop = Raindrop(self)
        drop_width, drop_height = drop.rect.size
        available_space_x = self.settings.screen_width - drop_width
        self.number_drops_x = available_space_x // (2 * drop_width)
        available_space_y = self.settings.screen_height
        number_rows = available_space_y // (2 * drop_height)
        for row_number in range(number_rows):
            self._create_row(row_number)
    def _create_row(self, row_number):
        for drop_number in range(self.number_drops_x):
            self._create_drop(drop_number, row_number)
    def _create_drop(self, drop_number, row_number):
        drop = Raindrop(self)
        drop_width, drop_height = drop.rect.size
        drop.rect.x = drop_width + 2 * drop_width * drop_number
        drop.y = 2 * drop.rect.height * row_number
        drop.rect.y = drop.y
        self.raindrops.add(drop)


    def _update_raindrops(self):
        self.raindrops.update()
        make_new_drops = False
        for drop in self.raindrops.copy():
            if drop.check_disappeared():
                self.raindrops.remove(drop)
                make_new_drops = True
            if make_new_drops:
                self._create_row(0)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.raindrops.draw(self.screen)
        pygame.display.flip()
if __name__ == '__main__':
    rd = RaindropsGame()
    rd.run_game()
clock = pygame.time.Clock()
clock.tick(120)