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
        self.camera = 0
        self.image = Surface((35, 35))
        self.image.fill(Color('Red'))
        self.rect = Rect(x, y, 35, 35)
        self.death_pos = (0, 0)
        self.on_ground = False
        self.direction = 'right'
        self.state = 'regular'
        self.platform_check = False
        self.frame = 0

    def update(self, left, right, run):
        if left:
            self.vel_x -= 0.4
            self.direction = 'left'
        if right:
            self.vel_x += 0.4
            self.direction = 'right'
        if not left and not right:
            if run:
                rang = 5
            else:
                rang = 4
            if self.vel_x <= 0.4:
                for i in range(rang):
                    if self.vel_x <= 0:
                        self.vel_x += 0.4
            elif self.vel_x >= 0.4:
                for i in range(rang):
                    if self.vel_x >= 0:
                        self.vel_x -= 0.4
            else:
                self.vel_x = 0
        if self.vel_x > 7 and not run:
            self.vel_x = 7
        elif self.vel_x < -7 and not run:
            self.vel_x = -7
        elif self.vel_x > 11 and run:
            self.vel_x = 11
        elif self.vel_x < -11 and run:
            self.vel_x = -11
        if not self.on_ground:
            self.vel_y += 0.5
        else:
            self.vel_y = 0

    def move(self, platforms, score, entities):
        self.rect.y += self.vel_y
        platforms, score = self.collision(0, self.vel_y, platforms, score)
        self.rect.x += self.vel_x
        platforms, score = self.collision(self.vel_x, 0, platforms, score)
        self.entity_collision(self.vel_x, self.vel_y, entities)
        camera = (-self.rect.x + 320, -self.rect.y + 240)
        return platforms, score, camera

    def collision(self, vel_x, vel_y, platforms, score):
        for p in platforms:
            if sprite.collide_rect(self, p[0]):
                if vel_x > 0 and p[1] != 'p':
                    self.rect.right = p[0].rect.left
                    self.vel_x = 0
                if vel_x < 0 and p[1] != 'p':
                    self.rect.left = p[0].rect.right
                    self.vel_x = 0
                if vel_y > 0:
                    self.rect.bottom = p[0].rect.top
                    self.on_ground = True
                    self.vel_y = 0
                if vel_y < 0 and p[1] != 'p':
                    self.rect.top = p[0].rect.bottom
                    self.vel_y = 0
                    if p[1] == 's' and vel_y < 0:
                        if p[2] == 1:
                            score += 100
                            platforms[platforms.index(p)] = (p[0], p[1], 0)
        else:
            self.on_ground = False
        return platforms, score

    def entity_collision(self, vel_x, vel_y, entities):
        for p in entities:
            if sprite.collide_rect(self, p):
                if vel_y > 0:
                    if p.type in ('deadly', 'hid', 'mv') and self.state == 'regular' and self.vel_y not in (0, 0.5, 1):
                        self.vel_y -= 15
                        if p.name == 'g':
                            p.type = 'dead'
                        elif p.name == 'k' and p.type == 'deadly':
                            p.type = 'hid'
                            p.vel_x = 0
                        else:
                            if self.direction == 'left':
                                p.vel_x -= 10
                                p.state = 'left'
                            else:
                                p.vel_x += 10
                                p.state = 'right'
                            p.type = 'mv'
                if vel_y < 0:
                    if p.type == 'deadly':
                        self.state = 'dead'
                        self.death_pos = (self.rect.x, self.rect.y)
                if vel_x > 0:
                    if p.type in ('deadly', 'mv') and self.vel_y in (0, 0.5, 1):
                        self.state = 'dead'
                        self.death_pos = (self.rect.x, self.rect.y)
                    else:
                        pass
                if vel_x < 0:
                    if p.type in ('deadly', 'mv') and self.vel_y in (0, 0.5, 1):
                        self.state = 'dead'
                        self.death_pos = (self.rect.x, self.rect.y)
                    else:
                        pass

    def death_animation(self):
        if self.frame == 0:
            self.vel_y -= 15
            self.rect.x, self.rect.y = self.death_pos[0], self.death_pos[1]
        if self.frame > 1:
            self.vel_y += 1.35
            self.rect.y += self.vel_y
        if self.frame == 30:
            print('a')
        self.frame += 1
