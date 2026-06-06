"""
🐞 СЛОМАЛОСЬ! Тут спрятан ОДИН баг.
Запусти файл. Змейка едет вправо, но стрелки её НЕ поворачивают!
Окно закрывается крестиком — значит события читаются. Прочитай строчку, которая
должна ловить «клавишу нажали» (KEYDOWN). С чем она сравнивает event.type?
Почини одной строчкой. Окно закрой крестиком.
"""
import pygame, sys

CELL = 20
COLS, ROWS = 30, 20
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS

BLACK = (30, 30, 46)
GREEN = (22, 196, 127)
DARK_GREEN = (0, 100, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

snake = [(5, 10), (4, 10), (3, 10)]
direction = (1, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.QUIT:
            # Меняем направление, но НЕ даём развернуться на 180°
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    snake.insert(0, new_head)
    snake.pop()

    screen.fill(BLACK)
    head_rect = pygame.Rect(snake[0][0] * CELL, snake[0][1] * CELL, CELL, CELL)
    pygame.draw.rect(screen, GREEN, head_rect)
    for segment in snake[1:]:
        rect = pygame.Rect(segment[0] * CELL, segment[1] * CELL, CELL, CELL)
        pygame.draw.rect(screen, DARK_GREEN, rect)

    pygame.display.flip()
    clock.tick(10)
