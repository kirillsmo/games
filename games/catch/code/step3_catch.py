"""
Урок 3: ловим яблоко и считаем очки.
Новое: pygame.Rect, colliderect() — проверка столкновения двух прямоугольников.
"""
import pygame, sys, random

WIDTH, HEIGHT = 600, 400
BG = (30, 30, 46)
ORANGE = (244, 162, 97)
RED = (230, 57, 70)
WHITE = (234, 234, 234)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловкий кот")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

cat_w, cat_h = 88, 74
cat_x = WIDTH // 2 - cat_w // 2
cat_y = HEIGHT - cat_h - 10

apple_w, apple_h = 46, 50
apple_x = random.randint(0, WIDTH - apple_w)
apple_y = -apple_h
speed = 4
score = 0

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

    apple_y += speed

    # Прямоугольники кота и яблока
    cat_rect = pygame.Rect(cat_x, cat_y, cat_w, cat_h)
    apple_rect = pygame.Rect(apple_x, apple_y, apple_w, apple_h)

    if cat_rect.colliderect(apple_rect):     # поймали!
        score += 1
        apple_x = random.randint(0, WIDTH - apple_w)
        apple_y = -apple_h
    elif apple_y > HEIGHT:                    # упало мимо
        apple_x = random.randint(0, WIDTH - apple_w)
        apple_y = -apple_h

    screen.fill(BG)
    pygame.draw.rect(screen, RED, apple_rect)
    pygame.draw.rect(screen, ORANGE, cat_rect)
    hud = font.render(f"Очки: {score}", True, WHITE)
    screen.blit(hud, (12, 10))
    pygame.display.flip()
    clock.tick(60)
