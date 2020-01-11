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
        self.vel_y = 0
        self.vel_x = 0
        self.image = Surface((40, 40))
        self.image.fill(Color('Brown'))
        self.rect = Rect(x, y, 40, 40)

    def update(self):
        if self.state == 'left':
            self.vel_x = -2
            self.last_state = 'left'
        if self.state == 'right':
            self.vel_x = 2
            self.last_state = 'right'
        if self.state == 'falling' and self.last_state == 'left':
            self.vel_y += 0.5
            self.vel_x = -2
        if self.state == 'falling' and self.last_state == 'right':
            self.vel_y += 0.5
            self.vel_x = 2
        self.rect.y += self.vel_y

    def move(self, platforms):
        self.update()
        self.collision(0, self.vel_y, platforms)
        self.rect.x += self.vel_x
        self.collision(self.vel_x, 0, platforms)

    def collision(self, vel_x, vel_y, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if vel_x > 0:
                    self.rect.right = p.rect.left
                    self.state = 'left'
                    self.last_state = 'left'
                    self.vel_x = 0
                if vel_x < 0:
                    self.rect.left = p.rect.right
                    self.state = 'right'
                    self.last_state = 'right'
                    self.vel_x = 0
                if vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.state = self.last_state
                    self.vel_y = 0
                if vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0
            else:
                self.state = 'falling'
