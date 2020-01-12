from pygame.sprite import Sprite
from pygame import sprite
from pygame import Surface
from pygame import Color
from pygame import Rect


class Goomba(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.last_state = 'left'
        self.state = 'left'
        self.type = 'deadly'
        self.name = 'g'
        self.vel_y = 0
        self.vel_x = 0
        self.image = Surface((35, 35))
        self.image.fill(Color('Brown'))
        self.rect = Rect(x, y, 35, 35)

    def update(self):
        if self.state == 'falling' and self.last_state == 'left':
            self.vel_y += 0.5
            if self.type == 'deadly':
                self.vel_x = -2
            elif self.type == 'mv':
                self.vel_x = -10
        if self.state == 'falling' and self.last_state == 'right':
            self.vel_y += 0.5
            if self.type == 'deadly':
                self.vel_x = 2
            elif self.type == 'mv':
                self.vel_x = 10
        if self.type == 'deadly':
            if self.state == 'left':
                self.vel_x = -2
                self.last_state = 'left'
            if self.state == 'right':
                self.vel_x = 2
                self.last_state = 'right'
        elif self.type == 'mv':
            if self.state == 'left':
                self.vel_x = -10
                self.last_state = 'left'
            if self.state == 'right':
                self.vel_x = 10
                self.last_state = 'right'
        self.rect.y += self.vel_y

    def move(self, platforms):
        self.update()
        self.collision(0, self.vel_y, platforms)
        self.rect.x += self.vel_x
        self.collision(self.vel_x, 0, platforms)

    def collision(self, vel_x, vel_y, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p[0]):
                if vel_x > 0:
                    self.rect.right = p[0].rect.left
                    self.state = 'left'
                    self.last_state = 'left'
                    self.vel_x = 0
                if vel_x < 0:
                    self.rect.left = p[0].rect.right
                    self.state = 'right'
                    self.last_state = 'right'
                    self.vel_x = 0
                if vel_y > 0:
                    self.rect.bottom = p[0].rect.top
                    self.state = self.last_state
                    self.vel_y = 0
                if vel_y < 0:
                    self.rect.top = p[0].rect.bottom
                    self.vel_y = 0
            else:
                self.state = 'falling'


class KoopaTroopa(Goomba):
    def __init__(self, x, y):
        Goomba.__init__(self, x, y)
        self.name = 'k'
        self.image.fill(Color('Green'))

    def move(self, platforms):
        self.update()
        self.collision(0, self.vel_y, platforms)
        self.rect.x += self.vel_x
        self.collision(self.vel_x, 0, platforms)

    def entity_collision(self, vel_x, entities):
        for p in entities:
            if sprite.collide_rect(self, p):
                if vel_x > 0 and p.vel_y in (0, 0.5, 1):
                    if p.type == 'deadly':
                        p.type = 'dead'
                    else:
                        pass
                if vel_x < 0 and p.vel_y in (0, 0.5, 1):
                    if p.type == 'deadly':
                        p.type = 'dead'
                    else:
                        pass
