from pygame.sprite import Sprite

from pygame import Surface
from pygame import Color
from pygame import Rect
from pygame import sprite


class Player(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.vel_x = 0
        self.vel_y = 0
        self.image = Surface((40, 40))
        self.image.fill(Color('Red'))
        self.rect = Rect(x, y, 40, 40)
        self.on_ground = False

    def update(self, left, right):
        if left:
            self.vel_x -= 0.2
        if right:
            self.vel_x += 0.2
        if not left and not right:
            if self.vel_x <= 0.2:
                for i in range(2):
                    if self.vel_x <= 0:
                        self.vel_x += 0.2
            elif self.vel_x >= 0.2:
                for i in range(2):
                    if self.vel_x >= 0:
                        self.vel_x -= 0.2
            else:
                self.vel_x = 0
        if not self.on_ground:
            self.vel_y += 0.35
        else:
            self.vel_y = 0

    def move(self, platforms):
        self.rect.y += self.vel_y
        self.collision(0, self.vel_y, platforms)
        self.rect.x += self.vel_x
        self.collision(self.vel_x, 0, platforms)

    def collision(self, vel_x, vel_y, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if vel_x > 0:
                    self.rect.right = p.rect.left
                    self.vel_x = 0
                if vel_x < 0:
                    self.rect.left = p.rect.right
                    self.vel_x = 0
                if vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                if vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0
            else:
                self.on_ground = False


