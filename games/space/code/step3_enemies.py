"""
Космос — шаг 3: появляются враги. Ещё один СПИСОК — врагов.
Стрелки — двигать корабль, Пробел — выстрел. (Пока пули врагов не задевают.)
"""
import pygame, sys, random

WIDTH, HEIGHT = 600, 400
BG = (15, 16, 38)
WHITE = (234, 234, 234)
SHIP_COLOR = (108, 178, 255)
BULLET_COLOR = (255, 209, 102)
ENEMY_COLOR = (255, 107, 107)

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
bullets = []

ENEMY_SIZE = 32
ENEMY_SPEED = 2
SPAWN_EVERY = 45                   # через сколько кадров появляется новый враг
enemies = []                      # СПИСОК врагов
spawn_timer = 0


def draw_enemy(e):
    """Пришелец — красный кружок с глазками."""
    ex, ey = e.center
    pygame.draw.circle(screen, ENEMY_COLOR, (ex, ey), ENEMY_SIZE // 2)
    pygame.draw.circle(screen, WHITE, (ex - 6, ey - 3), 4)
    pygame.draw.circle(screen, WHITE, (ex + 6, ey - 3), 4)
    pygame.draw.circle(screen, BG, (ex - 6, ey - 3), 2)
    pygame.draw.circle(screen, BG, (ex + 6, ey - 3), 2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(pygame.Rect(ship_x - BULLET_W // 2, ship_y, BULLET_W, BULLET_H))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_x -= SHIP_SPEED
    if keys[pygame.K_RIGHT]:
        ship_x += SHIP_SPEED
    ship_x = max(SHIP_W // 2, min(ship_x, WIDTH - SHIP_W // 2))

    # Пули летят вверх
    for b in bullets[:]:
        b.y -= BULLET_SPEED
        if b.bottom < 0:
            bullets.remove(b)

    # Каждые SPAWN_EVERY кадров ДОБАВЛЯЕМ нового врага в случайном месте сверху
    spawn_timer += 1
    if spawn_timer >= SPAWN_EVERY:
        spawn_timer = 0
        x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemies.append(pygame.Rect(x, -ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE))

    # Враги летят вниз; улетевших за низ УБИРАЕМ из списка
    for e in enemies[:]:
        e.y += ENEMY_SPEED
        if e.top > HEIGHT:
            enemies.remove(e)

    screen.fill(BG)
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b)
    for e in enemies:
        draw_enemy(e)
    points = [(ship_x, ship_y), (ship_x - SHIP_W // 2, ship_y + SHIP_H), (ship_x + SHIP_W // 2, ship_y + SHIP_H)]
    pygame.draw.polygon(screen, SHIP_COLOR, points)
    pygame.draw.circle(screen, WHITE, (ship_x, ship_y + SHIP_H - 8), 4)
    pygame.display.flip()
    clock.tick(60)
