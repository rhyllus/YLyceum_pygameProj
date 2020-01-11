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

    def update(self, left, right, run):
        if left:
            self.vel_x -= 0.4
        if right:
            self.vel_x += 0.4
        if not left and not right:
            if self.vel_x <= 0.4:
                for i in range(4):
                    if self.vel_x <= 0:
                        self.vel_x += 0.4
            elif self.vel_x >= 0.4:
                for i in range(4):
                    if self.vel_x >= 0:
                        self.vel_x -= 0.4
            else:
                self.vel_x = 0
        if self.vel_x > 7 and not run:
            self.vel_x = 7
        elif self.vel_x < -7 and not run:
            self.vel_x = -7
        elif self.vel_x > 10 and run:
            self.vel_x = 10
        elif self.vel_x < -10 and run:
            self.vel_x = -10
        if not self.on_ground:
            self.vel_y += 0.5
        else:
            self.vel_y = 0

    def move(self, platforms, score):
        self.rect.y += self.vel_y
        platforms, score = self.collision(0, self.vel_y, platforms, score)
        self.rect.x += self.vel_x
        platforms, score = self.collision(self.vel_x, 0, platforms, score)
        return platforms, score

    def collision(self, vel_x, vel_y, platforms, score):
        for p in platforms:
            if sprite.collide_rect(self, p[0]):
                if vel_x > 0:
                    self.rect.right = p[0].rect.left
                    self.vel_x = 0
                if vel_x < 0:
                    self.rect.left = p[0].rect.right
                    self.vel_x = 0
                if vel_y > 0:
                    self.rect.bottom = p[0].rect.top
                    self.on_ground = True
                    self.vel_y = 0
                if vel_y < 0:
                    self.rect.top = p[0].rect.bottom
                    self.vel_y = 0
                if p[1] == 's' and vel_y < 0:
                    if p[2] == 1:
                        score += 100
                        platforms[platforms.index(p)] = (p[0], p[1], 0)
            else:
                self.on_ground = False
        return platforms, score
