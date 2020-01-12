from pygame.sprite import Sprite
from pygame import Surface, image
from pygame import Color
from pygame import Rect


class MovingPlatform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.last_state = 'up'
        self.state = 'up'
        self.vel_y = 0
        self.vel_x = 0
        self.moved = 0
        self.original_y = y
        self.image = Surface((160, 20))
        self.image.fill(Color('Orange'))
        self.rect = Rect(x, y, 160, 20)

    def update(self):
        if self.rect.y == 40:
            self.rect.y = 520
            self.moved = 0
        self.rect.y -= 1
        self.moved += 1


class CoinBox(Sprite):
    def __init__(self, x, y, tile=None):
        Sprite.__init__(self)
        if tile is not None:
            self.image = image.load(tile)
        else:
            self.image = Surface((40, 40))
            self.image.fill((210, 60, 60))
        self.rect = Rect(x, y, 40, 40)
