"""
Урок 1: открываем окно.
Запуск:  python step1_window.py
Закрыть: крестик в углу окна.
"""
import pygame, sys

# Размер окна в пикселях
WIDTH = 600
HEIGHT = 400

# Цвет фона (Red, Green, Blue) — числа от 0 до 255
BLACK = (30, 30, 46)

# Готовим pygame и создаём окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Главный цикл игры — повторяется, пока окно открыто
while True:

    # 1. Смотрим, что нажал пользователь
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 2. Заливаем экран фоном
    screen.fill(BLACK)

    # 3. Показываем нарисованное
    pygame.display.flip()

    # 4. Ждём, чтобы было 60 кадров в секунду
    clock.tick(60)
