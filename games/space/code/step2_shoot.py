"""
Космос — шаг 2: корабль стреляет. ⭐ Главная новая идея — СПИСОК пуль.
Стрелки — двигать корабль, Пробел — выстрел.
"""
import pygame, sys

WIDTH, HEIGHT = 600, 400
BG = (15, 16, 38)
WHITE = (234, 234, 234)
SHIP_COLOR = (108, 178, 255)
BULLET_COLOR = (255, 209, 102)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космос")
clock = pygame.time.Clock()

SHIP_W, SHIP_H = 40, 28
ship_x = WIDTH // 2
ship_y = HEIGHT - SHIP_H - 12
SHIP_SPEED = 6

BULLET_W, BULLET_H = 4, 14
BULLET_SPEED = 9
bullets = []                       # СПИСОК пуль — пуль может быть много сразу

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # выстрел — ДОБАВЛЯЕМ новую пулю в список
            bullets.append(pygame.Rect(ship_x - BULLET_W // 2, ship_y, BULLET_W, BULLET_H))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_x -= SHIP_SPEED
    if keys[pygame.K_RIGHT]:
        ship_x += SHIP_SPEED
    ship_x = max(SHIP_W // 2, min(ship_x, WIDTH - SHIP_W // 2))

    # каждая пуля летит вверх; улетевшую за экран УБИРАЕМ из списка
    for b in bullets[:]:           # bullets[:] — копия списка, чтобы безопасно удалять
        b.y -= BULLET_SPEED
        if b.bottom < 0:
            bullets.remove(b)

    screen.fill(BG)
    for b in bullets:              # рисуем каждую пулю из списка
        pygame.draw.rect(screen, BULLET_COLOR, b)
    points = [(ship_x, ship_y), (ship_x - SHIP_W // 2, ship_y + SHIP_H), (ship_x + SHIP_W // 2, ship_y + SHIP_H)]
    pygame.draw.polygon(screen, SHIP_COLOR, points)
    pygame.draw.circle(screen, WHITE, (ship_x, ship_y + SHIP_H - 8), 4)
    pygame.display.flip()
    clock.tick(60)
