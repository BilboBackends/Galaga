class Settings:
    #a class to store all settings

    def __init__(self):

        #bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #alien_settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 5
        #fleet movement 1 is right -1 is left
        self.fleet_direction = 1

        #how fast the game speeds up, difficulty scaling
        self.speedup_scale = 1.1
        #how fast points for aliens increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #initializes settings that change in the game
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        #increase speed lul
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
