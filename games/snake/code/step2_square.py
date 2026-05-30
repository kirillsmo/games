"""
Урок 2: рисуем один зелёный квадрат на сетке.
Новое: сетка (клетки), pygame.Rect, pygame.draw.rect.
"""
import pygame, sys

# Игровое поле — сетка из клеток
CELL = 20          # размер одной клетки в пикселях
COLS = 30          # сколько клеток по горизонтали
ROWS = 20          # сколько клеток по вертикали
WIDTH = CELL * COLS   # 600
HEIGHT = CELL * ROWS  # 400

BLACK = (30, 30, 46)
GREEN = (22, 196, 127)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Координаты квадрата В КЛЕТКАХ (не в пикселях!)
x = 5
y = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Превращаем клетки в пиксели: умножаем на размер клетки
    rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
    pygame.draw.rect(screen, GREEN, rect)

    pygame.display.flip()
    clock.tick(60)
