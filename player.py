from pygame.sprite import Sprite

from pygame import Surface


class Player(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.img = Surface((22, 32))
        self.x = x
        self.y = y

    def update(self, left, right):
        if left:
            pass
        else:
            pass
