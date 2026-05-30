"""
Урок 4: змейка двигается сама.
Главный трюк: добавляем новую голову СПЕРЕДИ и убираем хвост — змейка "ползёт".
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

# Направление движения: (dx, dy)
# (1, 0) — вправо, (-1, 0) — влево, (0, 1) — вниз, (0, -1) — вверх
direction = (1, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Считаем новую голову: старая голова + направление
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Вставляем новую голову в начало списка, убираем хвост
    snake.insert(0, new_head)
    snake.pop()

    screen.fill(BLACK)
    head_rect = pygame.Rect(snake[0][0] * CELL, snake[0][1] * CELL, CELL, CELL)
    pygame.draw.rect(screen, GREEN, head_rect)
    for segment in snake[1:]:
        rect = pygame.Rect(segment[0] * CELL, segment[1] * CELL, CELL, CELL)
        pygame.draw.rect(screen, DARK_GREEN, rect)

    pygame.display.flip()
    clock.tick(10)  # 10 кадров в секунду — иначе змейка улетит
