import pygame


class Board:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.turn = 0
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        a = self.cell_size
        for j in range(1, self.height + 1):
            for i in range(1, self.width + 1):
                if self.board[i - 1][j - 1] == 0:
                    col = 1
                    color = (255, 255, 255)
                    pygame.draw.rect(screen, color,
                                     (self.left + i * a, self.top + j * a, a, a), col)
                else:
                    if self.turn % 2 == 1:
                        color = (0, 0, 255)
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (self.left + i * a, self.top + j * a, a, a), 1)
                        pygame.draw.line(screen, color, (self.left + i * a, self.top + j * a),
                                         (self.left + i * a + a, self.top + j * a + a), 1)
                        pygame.draw.line(screen, color, (self.left + i * a + a, self.top + j * a),
                                         (self.left + i * a, self.top + j * a + a), 1)
                    else:
                        color = (255, 0, 0)
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (self.left + i * a, self.top + j * a, a, a), 1)
                        pygame.draw.circle(screen, color,
                                           (self.left + i * a + a // 2, self.top + j * a + a // 2), a // 2 - 1, 1)
        pygame.display.flip()

    def addTurn(self):
        self.turn += 1

    def get_cell(self, mouse_pos):
        x = ((mouse_pos[0] - self.left) // self.cell_size) - 1
        y = ((mouse_pos[1] - self.top) // self.cell_size) - 1
        if x in range(self.width) and y in range(self.height):
            return (x, y)
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords != None:
            a = self.cell_size
            b = self.board[cell_coords[0]][cell_coords[1]]
            fill = 0
            color = (255, 0, 0)
            if b == 0:
                fill = 1
            else:
                fill = 1
                if b == 1:
                    color = (255, 0, 0)
                elif b == 2:
                    color = (0, 255, 0)
                elif b == 3:
                    color = (0, 0, 255)
            self.board[cell_coords[0]][cell_coords[1]] += 1
            pygame.draw.rect(screen, color,
                             (self.left + cell_coords[0] * a, self.top + cell_coords[1] * a, a, a),
                             fill)
        pygame.display.flip()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


board = Board(10, 10)
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.addTurn()
            board.get_click(event.pos)
    screen.fill((0, 0, 0))

    board.render()
    pygame.display.flip()

pygame.init()
pygame.quit()
