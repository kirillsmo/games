"""
Космос — шаг 1: корабль ездит влево-вправо.
Стрелки влево/вправо — двигать корабль.
"""
import pygame, sys

WIDTH, HEIGHT = 600, 400
BG = (15, 16, 38)
WHITE = (234, 234, 234)
SHIP_COLOR = (108, 178, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космос")
clock = pygame.time.Clock()

SHIP_W, SHIP_H = 40, 28
ship_x = WIDTH // 2                 # ship_x — это ЦЕНТР корабля
ship_y = HEIGHT - SHIP_H - 12
SHIP_SPEED = 6

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_x -= SHIP_SPEED
    if keys[pygame.K_RIGHT]:
        ship_x += SHIP_SPEED
    ship_x = max(SHIP_W // 2, min(ship_x, WIDTH - SHIP_W // 2))

    screen.fill(BG)
    # корабль — синий треугольник носом вверх
    points = [(ship_x, ship_y), (ship_x - SHIP_W // 2, ship_y + SHIP_H), (ship_x + SHIP_W // 2, ship_y + SHIP_H)]
    pygame.draw.polygon(screen, SHIP_COLOR, points)
    pygame.draw.circle(screen, WHITE, (ship_x, ship_y + SHIP_H - 8), 4)
    pygame.display.flip()
    clock.tick(60)
