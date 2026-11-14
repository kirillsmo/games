"""
Умная змейка-бот (курс «ИИ и игры», урок 8 — решение задания): змейка из курса «Змейка», но играть
может КОМПЬЮТЕР. Это «игровой ИИ» — не нейросеть, а несколько правил:
  1) посмотри на 3 клетки вокруг головы (вперёд, влево, вправо);
  2) выкинь опасные — стену и своё тело;
  3) НОВОЕ: не лезь в «мешок» — клетку, откуда мало свободного места;
  4) из оставшихся выбери ту, что ближе к яблоку.
B — включить/выключить бота. Стрелки — играть самому, пробел — заново.
F — полный экран, ESC — выход.
"""
import pygame, sys, random

CELL = 20
COLS, ROWS = 30, 20
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS

BLACK = (30, 30, 46)
GREEN = (22, 196, 127)
DARK_GREEN = (0, 100, 0)
RED = (255, 107, 107)
WHITE = (234, 234, 234)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fullscreen = False
pygame.display.set_caption("Змейка-бот")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 28)


def spawn_food(snake):
    """Случайная клетка, в которой нет змейки."""
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


def new_game():
    snake = [(5, 10), (4, 10), (3, 10)]
    direction = (1, 0)
    score = 0
    food = spawn_food(snake)
    return snake, direction, score, food


def is_safe(cell, snake):
    """Клетка безопасна, если она в поле и в ней нет тела змейки."""
    x, y = cell
    inside = 0 <= x < COLS and 0 <= y < ROWS
    return inside and cell not in snake


def distance(a, b):
    """Сколько шагов до цели, если ходить только по клеткам (без диагоналей)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def free_space(start, snake):
    """Сколько свободных клеток можно обойти, начав со start (заливка)."""
    body = set(snake)
    seen = {start}
    todo = [start]
    while todo:
        x, y = todo.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            cell = (nx, ny)
            if cell in seen or cell in body:
                continue
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                seen.add(cell)
                todo.append(cell)
    return len(seen)


def bot_choose(snake, direction, food):
    """МОЗГ БОТА: выбирает направление на этот ход."""
    head_x, head_y = snake[0]
    dx, dy = direction
    options = [(dx, dy), (dy, -dx), (-dy, dx)]   # вперёд, налево, направо

    best = direction          # если хороших ходов нет — едем прямо (и проиграем)
    best_score = None
    for d in options:
        cell = (head_x + d[0], head_y + d[1])
        if not is_safe(cell, snake):
            continue                              # туда нельзя — пропускаем
        room = free_space(cell, snake)
        roomy = room >= len(snake)                # места хватит, чтобы не застрять
        # Сначала важнее «просторно», потом «ближе к яблоку», потом «больше места»
        score = (roomy, -distance(cell, food), room)
        if best_score is None or score > best_score:
            best, best_score = d, score
    return best


def draw_food(screen, food):
    """Рисует яблоко красным квадратом."""
    rect = pygame.Rect(food[0] * CELL, food[1] * CELL, CELL, CELL)
    pygame.draw.rect(screen, RED, rect)


def draw_snake(screen, snake):
    """Рисует голову ярко-зелёным, а хвост — тёмным."""
    head_rect = pygame.Rect(snake[0][0] * CELL, snake[0][1] * CELL, CELL, CELL)
    pygame.draw.rect(screen, GREEN, head_rect)
    for segment in snake[1:]:
        rect = pygame.Rect(segment[0] * CELL, segment[1] * CELL, CELL, CELL)
        pygame.draw.rect(screen, DARK_GREEN, rect)


snake, direction, score, food = new_game()
game_over = False
bot_on = True             # бот играет сразу; B — переключить

while True:
    # 1. События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:                 # F — полный экран вкл/выкл
                fullscreen = not fullscreen
                flags = (pygame.SCALED | pygame.FULLSCREEN) if fullscreen else 0
                screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_b:               # B — бот вкл/выкл
                bot_on = not bot_on
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:
                snake, direction, score, food = new_game()
                game_over = False
                pygame.display.set_caption("Змейка-бот")
            elif event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # 2. Ход бота: он просто выбирает direction вместо стрелок
    if bot_on and not game_over:
        direction = bot_choose(snake, direction, food)

    # 3. Движение и столкновения
    if not game_over:
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        hit_wall = (
            new_head[0] < 0 or new_head[0] >= COLS
            or new_head[1] < 0 or new_head[1] >= ROWS
        )
        hit_self = new_head in snake

        if hit_wall or hit_self:
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += 1
                food = spawn_food(snake)
                pygame.display.set_caption(f"Змейка-бот — {score}")
            else:
                snake.pop()

    # 4. Рисование
    screen.fill(BLACK)
    draw_food(screen, food)
    draw_snake(screen, snake)

    mode = font_small.render("БОТ (B)" if bot_on else "ТЫ (B)", True, WHITE)
    screen.blit(mode, (8, 6))

    if game_over:
        text = font.render("Игра окончена! Пробел — заново", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(10)
