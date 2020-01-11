from pygame.sprite import Sprite
from pygame import Surface
from pygame import Color
from pygame import Rect


class MovingPlatform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.last_state = 'up'
        self.state = 'up'
        self.vel_y = 0
        self.vel_x = 0
        self.image = Surface((160, 20))
        self.image.fill(Color('Orange'))
        self.rect = Rect(x, y, 160, 20)

    def update(self):
        self.rect.y -= 0.5

