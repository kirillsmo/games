"""
Урок 3: змейка — это список клеток.
Новое: список координат, цикл for по списку, голова и хвост.
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

# Змейка = список клеток. Первая клетка — голова, остальные — хвост.
snake = [(5, 10), (4, 10), (3, 10)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Рисуем голову ярко-зелёным
    head_x, head_y = snake[0]
    head_rect = pygame.Rect(head_x * CELL, head_y * CELL, CELL, CELL)
    pygame.draw.rect(screen, GREEN, head_rect)

    # Рисуем хвост тёмно-зелёным. snake[1:] — все клетки кроме первой.
    for segment in snake[1:]:
        seg_x, seg_y = segment
        rect = pygame.Rect(seg_x * CELL, seg_y * CELL, CELL, CELL)
        pygame.draw.rect(screen, DARK_GREEN, rect)

    pygame.display.flip()
    clock.tick(60)
