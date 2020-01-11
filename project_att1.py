import pygame
from player import Player

size_w = (640, 480)
size_lv = (2800, 2800)
window = pygame.display.set_mode(size_w)
screen = pygame.Surface(size_lv)
running = True
pygame.init()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, tile=None):
        pygame.sprite.Sprite.__init__(self)
        if tile is not None:
            self.image = pygame.image.load(tile)
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill((210, 120, 60))
        self.rect = pygame.Rect(x, y, 40, 40)


class CoinBox(pygame.sprite.Sprite):
    def __init__(self, x, y, tile=None):
        pygame.sprite.Sprite.__init__(self)
        if tile is not None:
            self.image = pygame.image.load(tile)
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill((210, 60, 60))
        self.rect = pygame.Rect(x, y, 40, 40)


def build_stage(level):
    x = 0
    y = 0
    for i in level:
        for j in i:
            if j == '1':
                pl = Platform(x, y)
                objects.append((pl, '1'))
                entities.add(pl)
            if j == 's':
                pl = CoinBox(x, y)
                objects.append((pl, 's', 1))
                entities.add(pl)
            x += 40
        y += 40
        x = 0


objects = []
level = ['1111111111111111111111111111111111111111',
         '1111111111111111111111111111111111111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111...111111111..............11111111',
         '111111..........................11111111',
         '111111..........................11111111',
         '111111..11ssssssssssss111111111.11111111',
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
score = 0
font = pygame.font.SysFont(None, 50)
build_stage(level)
left = right = jump = run = False
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
            if event.key == 304:
                run = True
            if event.key == pygame.K_UP:
                if abs(player.vel_y) in [0, 0.5, 1]:
                    player.vel_y -= 12
                    player.on_ground = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == 304:
                run = False
    screen.fill((100, 255, 100))
    player.update(left, right, run)
    objects, score = player.move(objects, score)
    entities.draw(screen)
    text_str = 'Score: {}'.format(score)
    text = font.render(text_str, 1, (0, 0, 0))
    text_x = player.rect.x + 150 - len(str(score)) * 10
    text_y = player.rect.y - 230
    screen.blit(text, (text_x, text_y))
    window.blit(screen, (-player.rect.x + 320, -player.rect.y + 240))
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
