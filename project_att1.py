import pygame
from player import Player

size_w = (640, 480)
size_lv = (2800, 2800)
window = pygame.display.set_mode(size_w)
screen = pygame.Surface(size_lv)
running = True


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, tile=None):
        pygame.sprite.Sprite.__init__(self)
        if tile is not None:
            self.image = pygame.image.load(tile)
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill((210, 120, 60))
        self.rect = pygame.Rect(x, y, 40, 40)


def build_stage(level):
    x = 0
    y = 0
    for i in level:
        for j in i:
            if j == '1':
                pl = Platform(x, y)
                platforms.append(pl)
                entities.add(pl)
            x += 40
        y += 40
        x = 0


platforms = []
level = ['1111111111111111111111111111111111111111',
         '1111111111111111111111111111111111111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111...111111111..............11111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111..11............111111111.11111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '1111111111111111111111111111111111111111',
         '1111111111111111111111111111111111111111',
         '1111111111111111111111111111111111111111',
         '1111111111111111111111111111111111111111',
         '1111111111111111111111111111111111111111'
         ]

player = Player(440, 440)
entities = pygame.sprite.Group()
entities.add(player)
build_stage(level)
left = right = jump = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_UP:
                a = abs(player.vel_y)
                if abs(player.vel_y) in [0, 0.35, 0.7]:
                    player.vel_y -= 10
                    player.on_ground = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
    screen.fill((100, 255, 100))
    player.update(left, right)
    player.move(platforms)
    clock.tick(60)
    entities.draw(screen)
    window.blit(screen, (-player.rect.x + 320, -player.rect.y + 240))
    pygame.display.flip()

pygame.init()
pygame.quit()
