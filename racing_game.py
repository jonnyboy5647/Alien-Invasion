import pygame
import sys
from pygame.sprite import Sprite
from random import random
from random import randint
from pygame import mixer


class Car:
    def __init__(self, rg_game):
        self.screen = rg_game.screen
        self.settings = rg_game.settings
        self.screen_rect = rg_game.screen.get_rect()
        self.image = pygame.image.load('images/car_black_3.png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.screen_rect.bottomleft
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.car_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.car_speed

        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Car2:
    def __init__(self, rg_game):
        self.screen = rg_game.screen
        self.settings = rg_game.settings
        self.screen_rect = rg_game.screen.get_rect()
        self.image = pygame.image.load('images/car_black_3.png')
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.screen_rect.bottomright
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.car_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.car_speed

        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (0, 0, 255)
        self.car_speed = 6
        self.bullet_speed = 8
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 10
        self.alien_speed = 7.5
        self.alien_frequency = 0.015
        self.car_limit = 0


class Bullet(Sprite):
    def __init__(self, rg_game):
        super().__init__()
        self.screen = rg_game.screen
        self.settings = rg_game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = rg_game.car.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Alien(Sprite):
    def __init__(self, ss_game):
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.image = pygame.image.load('images/redmot.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen.get_rect().top
        alien_top_max = self.settings.screen_width - self.rect.width
        self.rect.left = randint(0, alien_top_max)
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.alien_speed
        self.rect.y = self.y


class GameStats:
    def __init__(self, rg_game):
        self.settings = rg_game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        self.cars_left = self.settings.car_limit


class Background:
    def __init__(self, jj_game):
        super().__init__()
        self.screen = jj_game.screen

        self.image = pygame.image.load("images/roadbacl.png")

        self.screen_rect = self.screen.get_rect
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class RacingGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((910, 1030))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Racing Game")
        self.car = Car(self)
        self.car2 = Car2(self)
        self.background = Background(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)

    def run_game(self):
        self._background_music()

        while self.stats.game_active:
            self._check_events()
            if self.stats.game_active:
                self.car.update()
                self.car2.update()
                self._update_bullets()
                self._update_aliens()
                self._create_alien()
            self._update_screen()

        Font = pygame.font.SysFont('Arial', 60)
        game_over_text = Font.render(f"GAME OVER", True, (200, 200, 200))
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, (300, 400))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

    def _background_music(self):
        pygame.mixer.music.load("music/Assets_Audio_music.ogg")
        pygame.mixer.music.play(-1)

    def _check_aliens_left_edge(self):
        for alien in self.aliens.sprites():
            if alien.rect.left < 0:
                self._car_hit()
                break

    def _car_hit(self):
        if self.stats.cars_left > 0:
            self.stats.cars_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            #self.car.center_car()
        else:
            self.stats.game_active = False


    def _create_alien(self):
        if random() < self.settings.alien_frequency:
            alien = Alien(self)
            self.aliens.add(alien)
            print(len(self.aliens))

        Font = pygame.font.SysFont('Arial', 30)
        score_text = Font.render(f"SCORE: {len(self.aliens)}", True, (0, 0, 0))
        self.screen.blit(score_text, (15, 20))

    def _update_aliens(self):
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.car, self.aliens):
            self._car_hit()
        if pygame.sprite.spritecollideany(self.car2, self.aliens):
            self._car_hit()
        self._check_aliens_left_edge()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.car.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.car.moving_left = True
        elif event.key == pygame.K_d:
            self.car2.moving_right = True
        elif event.key == pygame.K_a:
            self.car2.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            bullet_sound = mixer.Sound("music/laser.wav")
            bullet_sound.play()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.car.moving_right = False
        elif event.key == pygame.K_d:
            self.car2.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.car.moving_left = False
        elif event.key == pygame.K_a:
            self.car2.moving_left = False

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.background.blitme()
        self.car.blitme()
        self.car2.blitme()
        self._create_alien()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    rg = RacingGame()
    rg.run_game()
