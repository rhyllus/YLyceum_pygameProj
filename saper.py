import pygame
import copy


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        print(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Minesweeper(Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = '0'

    def render(self):
        left, top, cell_size = self.left, self.top, self.cell_size
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == 0:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (x * cell_size + left,
                                      y * cell_size + top, cell_size,
                                      cell_size), 1)
                elif self.board[x][y] == 10:
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (x * cell_size + left,
                                      y * cell_size + top, cell_size,
                                      cell_size), 0)

    def get_click(self, mouse_pos):
        font = pygame.font.Font(None, 50)
        cell = self.get_cell(mouse_pos)
        if self.board[cell[0]][cell[1]] == 0 and self.game_state == '0':
            self.board[cell[0]][cell[1]] = (self.board[cell[0]][cell[1]] + 1) % 2 * 10
        elif self.board[cell[0]][cell[1]] == 0 and self.game_state == '1':
            screen.blit(font.render("{}".format(self.next_move()), 1, (0, 255, 0)),
                        (0, 0))

    def next_move(self):
        summ = 0
        for y in range(self.height):
            for x in range(self.width):
                for i in range(y - 1, y + 2):
                    for j in range(x - 1, x + 2):
                        if not (j < 0 or i < 0) and not (j >= self.width or i >= self.height):
                            summ += self.board[i][j] // 10
                summ -= self.board[y][x]
        return abs(summ)


pygame.init()
board = Minesweeper(10, 10)
clock = pygame.time.Clock()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN and event.key == 32) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
            if board.game_state == '0':
                board.game_state = '1'
            else:
                board.game_state = '0'
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    clock.tick(10)
    pygame.display.flip()

pygame.quit()
