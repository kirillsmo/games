"""
Урок 2: сверху падает яблоко.
Новое: объект с координатами, постоянное движение вниз, возврат наверх.
"""
import pygame, sys, random

WIDTH, HEIGHT = 600, 400
BG = (30, 30, 46)
ORANGE = (244, 162, 97)
RED = (230, 57, 70)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловкий кот")
clock = pygame.time.Clock()

cat_w, cat_h = 88, 74
cat_x = WIDTH // 2 - cat_w // 2
cat_y = HEIGHT - cat_h - 10

# Яблоко
apple_w, apple_h = 46, 50
apple_x = random.randint(0, WIDTH - apple_w)
apple_y = -apple_h          # начинаем чуть выше экрана
speed = 4                   # на сколько пикселей падает за кадр

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cat_x -= 7
    if keys[pygame.K_RIGHT]:
        cat_x += 7
    cat_x = max(0, min(cat_x, WIDTH - cat_w))

    # Яблоко падает
    apple_y += speed
    # Улетело вниз — заводим новое сверху в случайном месте
    if apple_y > HEIGHT:
        apple_x = random.randint(0, WIDTH - apple_w)
        apple_y = -apple_h

    screen.fill(BG)
    pygame.draw.rect(screen, RED, (apple_x, apple_y, apple_w, apple_h))
    pygame.draw.rect(screen, ORANGE, (cat_x, cat_y, cat_w, cat_h))
    pygame.display.flip()
    clock.tick(60)
