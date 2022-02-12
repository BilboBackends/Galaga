import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #representing single alien

    def __init__(self, ai_game):
        #initializing alien and start position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #load alien image and set rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

     #spawning alien at top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

     #storing horizontal position
        self.x = float(self.rect.x)


    def check_edges(self):
       #returns true if alien is at edge of screen
       screen_rect = self.screen.get_rect()
       if self.rect.right >= screen_rect.right or self.rect.left <= 0:
          return True

    def update(self):
         #move alien left and right
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    