
import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    #managing game asset behavior

    def __init__(self):
        pygame.init()
        #making screen
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode(
           (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
       

    def run_game(self):
            #updating screen
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()
            #getting rid of bullets
            self._update_bullets()
            self._update_screen()
            

    def _check_events(self):
        #responds to keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)             
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        #start game when click play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            #hide cursor
            pygame.mouse.set_visible(False)

    def  _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
                    #move ship right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
             

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #create bullet and add to bullet group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 

    def _update_bullets(self):
        #update position of bullets and delete old ones
        #update bullet position
        self.bullets.update()
        #get rid of old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
      

    def _check_bullet_alien_collision(self):
        #responds to bullet and alien collisions and removes them if so
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #destroy existing bullets and make new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        #respond to ship being hit by alien
        if self.stats.ships_left > 0:
            #decrements ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            #create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            #pausing
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            

    def _update_aliens(self):
        #checks if fleet at an edge and updates all aliens
        self._check_fleet_edges()
        self.aliens.update()
        #look for alien and ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #look for aliens at bottom of screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        #make fleet of aliens
        #making an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        #determine number of rows of aliens that fit on a screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        #create fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #creating alien and placing it in row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        #responds when an alien hits the edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        #check if aliens hit the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        #drops aliens and changes direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        #draw playbutton if game inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

#running game
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
