import pygame
from player import Player

size = (640, 480)
window = pygame.display.set_mode(size)
screen = pygame.Surface(size)
running = True


class Platform:
    def __init__(self, tile=None):
        if tile is not None:
            self.img = pygame.image.load(tile)


def build_stage(level, tile):
    x = 0
    y = 0
    for i in level:
        for j in i:
            if j == '1':
                screen.blit(tile, (x, y))
            x += 40
        y += 40
        x = 0


level = ['1111111111111111',
         '1..............1',
         '1..............1',
         '1..............1',
         '1..............1',
         '1..............1',
         '1..1111........1',
         '1..............1',
         '1..............1',
         '1.........11...1',
         '1..............1',
         '1111111111111111'
         ]

pl = pygame.Surface((40, 40))
pl.fill((210, 120, 60))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.KEYUP:
            pass
        screen.fill((100, 255, 100))
        build_stage(level, pl)
        Player.update(Player(10, 10), True, True)
        window.blit(screen, (0, 0))
        pygame.display.flip()

pygame.init()
