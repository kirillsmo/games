"""
Змейка — финальная версия.
Стрелки — управление, пробел — заново после проигрыша.
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
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
fullscreen = False
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)


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


snake, direction, score, food = new_game()
game_over = False

while True:
    # 1. События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:                 # F — полный экран вкл/выкл
                fullscreen = not fullscreen
                flags = pygame.SCALED | (pygame.FULLSCREEN if fullscreen else 0)
                screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:
                snake, direction, score, food = new_game()
                game_over = False
                pygame.display.set_caption("Змейка")
            elif event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # 2. Движение и столкновения
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
                pygame.display.set_caption(f"Змейка — {score}")
            else:
                snake.pop()

    # 3. Рисование
    screen.fill(BLACK)

    food_rect = pygame.Rect(food[0] * CELL, food[1] * CELL, CELL, CELL)
    pygame.draw.rect(screen, RED, food_rect)

    head_rect = pygame.Rect(snake[0][0] * CELL, snake[0][1] * CELL, CELL, CELL)
    pygame.draw.rect(screen, GREEN, head_rect)
    for segment in snake[1:]:
        rect = pygame.Rect(segment[0] * CELL, segment[1] * CELL, CELL, CELL)
        pygame.draw.rect(screen, DARK_GREEN, rect)

    if game_over:
        text = font.render("Игра окончена! Пробел — заново", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(10)
