import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна и игрового поля
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 900
GRID_SIZE = 8
CELL_SIZE = (WINDOW_WIDTH - 400) // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Фигуры из тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1], [1], [1], [1]],  # I
    [[1, 1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # O
    # [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Block Blast")
# Шрифт для текста
font = pygame.font.Font(None, 36)

# Игровое поле
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
# Счёт
score = 0
shapes = []


# Функция для создания новой фигуры
def create_shape():
    global shapes
    if shapes:
        return shapes
    else:
        for pos in range(3):
            shape = random.choice(SHAPES)
            color = random.choice(COLORS)
            shapes.append({'shape': shape, 'color': color, 'x': 4 * pos + 1, 'y': GRID_SIZE})
        return shapes


# Функция для отрисовки сетки
def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], rect.inflate(-4, -4))


# Функция для отрисовки фигуры
def draw_shape(shape, x, y):
    for row in range(len(shape['shape'])):
        for col in range(len(shape['shape'][row])):
            if shape['shape'][row][col]:
                rect = pygame.Rect((x + col) * CELL_SIZE, (y + row) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, shape['color'], rect.inflate(-4, -4))


# Функция для проверки, можно ли разместить фигуру на поле
def can_place_shape(shape, x, y):
    for row in range(len(shape['shape'])):
        for col in range(len(shape['shape'][row])):
            if shape['shape'][row][col]:
                if x + col < 0 or x + col >= GRID_SIZE or y + row >= GRID_SIZE or grid[y + row][x + col]:
                    return False
    return True


# Функция для размещения фигуры на поле
def place_shape(shape, x, y):
    for row in range(len(shape['shape'])):
        for col in range(len(shape['shape'][row])):
            if shape['shape'][row][col]:
                grid[y + row][x + col] = shape['color']


# Функция для проверки и удаления заполненных строк и столбцов
def check_lines():
    global score
    global grid
    # Проверка строк
    rows_to_remove = []
    for y in range(GRID_SIZE):
        if all(grid[y][x] for x in range(GRID_SIZE)):
            rows_to_remove.append(y)
    # Проверка столбцов
    cols_to_remove = []
    for x in range(GRID_SIZE):
        if all(grid[y][x] for y in range(GRID_SIZE)):
            cols_to_remove.append(x)
    # Удаление строк
    for y in rows_to_remove:
        for x in range(GRID_SIZE):
            grid[y][x] = 0
    # Удаление столбцов
    for x in cols_to_remove:
        for y in range(GRID_SIZE):
            grid[y][x] = 0
    score += len(rows_to_remove) + len(cols_to_remove)


# Функция для сброса игры
def reset_game():
    global grid, score, shapes
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    score = 0
    shapes = []
    create_shape()


# Функция для отрисовки счёта
def draw_score():
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    screen.blit(score_text, (10, WINDOW_HEIGHT - 50))


# Функция для отрисовки кнопки рестарта
def draw_restart_button():
    button_rect = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50, 140, 40)
    pygame.draw.rect(screen, RED, button_rect)
    restart_text = font.render("Рестарт", True, WHITE)
    screen.blit(restart_text, (WINDOW_WIDTH - 140, WINDOW_HEIGHT - 45))


# Основной цикл игры
create_shape()
dragging = -1
offset_x, offset_y = 0, 0

running = True
while running:
    screen.fill(BLACK)
    draw_grid()
    draw_score()
    draw_restart_button()
    for current_shape in shapes:
        draw_shape(current_shape, current_shape['x'], current_shape['y'])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if WINDOW_WIDTH - 150 <= mouse_x <= WINDOW_WIDTH - 10 and WINDOW_HEIGHT - 50 <= mouse_y <= WINDOW_HEIGHT - 10:
                reset_game()

            for i, current_shape in enumerate(shapes):
                shape_x = current_shape['x'] * CELL_SIZE
                shape_y = current_shape['y'] * CELL_SIZE
                shape_width = len(current_shape['shape'][0]) * CELL_SIZE
                shape_height = len(current_shape['shape']) * CELL_SIZE
                if shape_x <= mouse_x <= shape_x + shape_width and shape_y <= mouse_y <= shape_y + shape_height:
                    dragging = i
                    offset_x = mouse_x - shape_x
                    offset_y = mouse_y - shape_y
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging > -1:
                current_shape = shapes[dragging]
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_x = (mouse_x - offset_x) // CELL_SIZE
                new_y = (mouse_y - offset_y) // CELL_SIZE
                if can_place_shape(current_shape, new_x, new_y):
                    place_shape(current_shape, new_x, new_y)
                    check_lines()
                    del shapes[dragging]
                    current_shape = create_shape()
                dragging = -1

        elif event.type == pygame.MOUSEMOTION and dragging > -1:
            current_shape = shapes[dragging]
            mouse_x, mouse_y = pygame.mouse.get_pos()
            current_shape['x'] = (mouse_x - offset_x) // CELL_SIZE
            current_shape['y'] = (mouse_y - offset_y) // CELL_SIZE

    pygame.display.flip()

pygame.quit()
