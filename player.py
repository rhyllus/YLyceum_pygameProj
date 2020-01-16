from pygame import Color
from pygame import Rect
from pygame import Surface
from pygame import sprite
from pygame.sprite import Sprite
from enemies import MagicMushroom


class Player(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.vel_x = 0
        self.vel_y = 0
        self.camera = 0
        self.image = Surface((40, 40))
        self.image.fill(Color('Red'))
        self.rect = Rect(x, y, 40, 40)
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

    def move(self, platforms, score, entities, current, sprites):
        self.rect.y += self.vel_y
        platforms, score, current, entities, sprites = self.collision(0, self.vel_y, platforms, score, current, entities, sprites)
        self.rect.x += self.vel_x
        platforms, score, current, entities2, sprites = self.collision(self.vel_x, 0, platforms, score, current, entities, sprites)
        score = self.entity_collision(self.vel_x, self.vel_y, entities, score)
        camera = (-self.rect.x + 320, -self.rect.y + 325)
        return platforms, score, camera, current, entities, sprites

    def collision(self, vel_x, vel_y, platforms, score, current, entities, sprites):
        for p in platforms:
            if sprite.collide_rect(self, p[0]):
                if p[1] == '/':
                    self.state = 'dead'
                    self.death_pos = (self.rect.x, self.rect.y)
                if p[1] == 'f':
                    current += 1
                if vel_x > 0 and p[1] != 'p':
                    self.rect.right = p[0].rect.left
                    self.vel_x = 0
                if vel_x < 0 and p[1] != 'p':
                    self.rect.left = p[0].rect.right
                    self.vel_x = 0
                if vel_y > 0:
                    if self.rect.bottom <= p[0].rect.bottom:
                        self.rect.bottom = p[0].rect.top
                        self.on_ground = True
                        self.vel_y = 0
                if vel_y < 0 and p[1] != 'p':
                    self.rect.top = p[0].rect.bottom
                    self.vel_y = 0
                    if p[1] == 's':
                        if p[2] == 1:
                            score += 100
                            platforms[platforms.index(p)] = (p[0], p[1], 0)
                    if p[1] == 'M':
                        if p[2] == 1:
                            pl = MagicMushroom(p[0].rect.x, p[0].rect.y - 40)
                            sprites.add(pl)
                            entities.append(pl)
                            platforms[platforms.index(p)] = (p[0], p[1], 0)
        else:
            self.on_ground = False
        return platforms, score, current, entities, sprites

    def entity_collision(self, vel_x, vel_y, entities, score):
        for p in entities:
            if sprite.collide_rect(self, p):
                if p.name == 'm':
                    p.name = '0'
                if vel_y > 0:
                    if p.type in ('deadly', 'hid', 'mv') and self.state != 'dead' and self.vel_y not in (
                            0, 0.5, 1):
                        self.vel_y = -5
                        score += 100
                        if p.name == 'g':
                            p.type = 'dead'
                        elif p.name == 'k' and p.type in ('deadly', 'mv'):
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
        return score

    def death_animation(self):
        if self.frame == 0:
            self.vel_y = 0
            self.rect.x, self.rect.y = self.death_pos[0], self.death_pos[1]
            self.vel_y = -15
        if self.frame > 1:
            self.vel_y += 1.35
            self.rect.y += self.vel_y
        if self.frame == 35:
            return True
        self.frame += 1
        return False
