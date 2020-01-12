import pygame
from player import Player
from objects import CoinBox, MovingPlatform
from enemies import Goomba, KoopaTroopa

size_w = (640, 480)
size_lv = (9000, 480)
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
            self.image = pygame.image.load(tile).convert()
            self.image = pygame.transform.scale(self.image, (40, 40))
        else:
            self.image = pygame.Surface((40, 40))
        self.rect = pygame.Rect(x, y, 40, 40)


def build_stage(level):
    global camera_border_x_left, camera_border_y_up, camera_border_x_right, camera_border_y_down
    x = 0
    y = 0
    for i in level:
        for j in i:
            if j in ('1', '2', '3', '4', '5', '6', '7'):
                pl = Platform(x, y, 'sprites/tile{}.png'.format(j))
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
            elif j == '/':
                pl = Platform(x, y)
                objects.append((pl, '/', 1))
            elif j == 'b':
                pl = Platform(x, y)
                objects.append((pl, '0', 1))
            x += 40
        y += 40
        x = 0


def load_level(filename):
    filename = 'levels/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def obj_update(objs):
    for obj in objs:
        if obj[1] in ('p', 's'):
            if obj[1] == 's' and objs[objs.index(obj)]:
                obj[0].update(obj[2])
            else:
                obj[0].update()
    return objs


objects = []
enemies = []
level = load_level('1-1.txt')

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
                    if abs(player.vel_y) in (0, 0.5, 1):
                        player.vel_y -= 14
                        player.on_ground = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                if abs(player.vel_y) not in (0, 0.5, 1):
                    if player.vel_y <= 0:
                        player.vel_y = -2
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == 304:
                run = False
    screen.fill((107, 140, 255))
    for enemy in enemies:
        if enemy.type == 'dead':
            entities.remove(enemy)
        elif abs(abs(enemy.rect.x) - abs(player.rect.x)) < 400:
            enemy.move(objects)
            if enemy.type == 'mv':
                score = enemy.entity_collision(enemy.vel_x, enemies, score)
    if player.state == 'dead':
        if player.death_animation():
            enemies.clear()
            score = 0
            entities = pygame.sprite.Group()
            objects.clear()
            player = Player(440, 440)
            entities.add(player)
            build_stage(level)
    else:
        objects, score, camera = player.move(objects, score, enemies)
        player.update(left, right, run)
    objects = obj_update(objects)
    entities.draw(screen)
    text_str = 'Score: {}'.format(score)
    text = font.render(text_str, 1, (0, 0, 0))
    if player.state != 'dead':
        text_x = -camera[0] + 465
        text_y = 10
    screen.blit(text, (text_x, text_y))
    window.blit(screen, (camera[0], 0))
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
