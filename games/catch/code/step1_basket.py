"""
Урок 1: кот-корзинка ездит влево-вправо.
Новое: движение в пикселях, pygame.key.get_pressed() (зажатые клавиши).
"""
import pygame, sys

WIDTH, HEIGHT = 600, 400
BG = (30, 30, 46)
ORANGE = (244, 162, 97)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловкий кот")
clock = pygame.time.Clock()

# Пока кот — это просто оранжевый прямоугольник
cat_w, cat_h = 88, 74
cat_x = WIDTH // 2 - cat_w // 2     # по центру
cat_y = HEIGHT - cat_h - 10         # внизу

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Зажатые клавиши: пока держишь — кот едет
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cat_x -= 7
    if keys[pygame.K_RIGHT]:
        cat_x += 7

    # Не выпускаем кота за края экрана
    cat_x = max(0, min(cat_x, WIDTH - cat_w))

    screen.fill(BG)
    pygame.draw.rect(screen, ORANGE, (cat_x, cat_y, cat_w, cat_h))
    pygame.display.flip()
    clock.tick(60)
