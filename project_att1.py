import pygame
from player import Player
from objects import CoinBox, MovingPlatform
from enemies import Goomba, KoopaTroopa

size_w = (640, 480)
size_lv = (2800, 2800)
window = pygame.display.set_mode(size_w)
screen = pygame.Surface(size_lv)
running = True
camera_border_x_left = 0
camera_border_x_right = 0
camera_border_y_up = 0
camera_border_y_down = 0
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


def build_stage(level):
    global camera_border_x_left, camera_border_y_up, camera_border_x_right, camera_border_y_down
    x = 0
    y = 0
    for i in level:
        for j in i:
            if j == '1':
                pl = Platform(x, y)
                objects.append((pl, '1'))
                entities.add(pl)
            elif j == 's':
                pl = CoinBox(x, y)
                objects.append((pl, 's', 1))
                entities.add(pl)
            elif j == 'p':
                pl = MovingPlatform(x, y)
                objects.append((pl, 'p', 1))
                entities.add(pl)
            elif j == 'g':
                pl = Goomba(x, y)
                enemies.append(pl)
                entities.add(pl)
            elif j == 'k':
                pl = KoopaTroopa(x, y)
                enemies.append(pl)
                entities.add(pl)
            elif j == 'X':
                camera_border_x_left = x
            elif j == 'Y':
                camera_border_y_up = y
            elif j == 'x':
                camera_border_x_left = x
            elif j == 'y':
                camera_border_y_down = y

            x += 40
        y += 40
        x = 0


def platform_update(objs):
    for obj in objs:
        if obj[1] == 'p':
            obj[0].update()
    return objs


objects = []
enemies = []
level = ['1111111111111111111111111111111111....111111111111',
         '1111111111111111111111111111111111....111111111111',
         '111111....................................11111111',
         '111111............................p.......11111111',
         '111111....................................11111111',
         '111111....................................11111111',
         '111111...111111111................p.......11111111',
         '111111....................................11111111',
         '111111....................................11111111',
         '111111..11..........11111111111...p.......11111111',
         '111111.................k.....g............11111111',
         '111111....................................11111111',
         '1111111111111111111111111111111111p...111111111111',
         '1111111111111111111111111111111111....111111111111',
         '1111111111111111111111111111111111....111111111111',
         '1111111111111111111111111111111111p...111111111111',
         '1111111111111111111111111111111111....111111111111'
         ]

player = Player(440, 440)
entities = pygame.sprite.Group()
entities.add(player)
score = 0
current = ''
camera = (0, 0)
font = pygame.font.SysFont(None, 50)
build_stage(level)
left = right = jump = run = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if player.state == 'regular':
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
    screen.fill((107, 140, 255))
    objects = platform_update(objects)
    for enemy in enemies:
        if enemy.type == 'dead':
            entities.remove(enemy)
        else:
            enemy.move(objects)
            if enemy.type == 'mv':
                enemy.entity_collision(enemy.vel_x, enemies)
    entities.draw(screen)
    if player.state == 'dead':
        player.death_animation()
    else:
        objects, score, camera = player.move(objects, score, enemies)
        player.update(left, right, run)
    text_str = 'Score: {}'.format(score)
    text = font.render(text_str, 1, (0, 0, 0))
    if player.state != 'dead':
        text_x = player.rect.x + 150 - len(str(score)) * 10
        text_y = player.rect.y - 230
    screen.blit(text, (text_x, text_y))
    window.blit(screen, camera)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
