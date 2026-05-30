"""
Урок 2: мяч летает и отскакивает от стен.
ГЛАВНАЯ новая идея: скорость мяча (dx, dy), отскок = смена знака.
Пока мяч отскакивает от ВСЕХ четырёх стен (даже от нижней).
"""
import pygame, sys

WIDTH, HEIGHT = 600, 400
BG = (30, 30, 46)
GREEN = (22, 196, 127)
BALL_COLOR = (255, 209, 102)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")
clock = pygame.time.Clock()

PADDLE_W, PADDLE_H = 90, 14
paddle_x = WIDTH // 2 - PADDLE_W // 2
paddle_y = HEIGHT - 30

# Мяч: позиция (bx, by) и скорость (dx, dy)
BALL_R = 8
bx, by = WIDTH / 2, HEIGHT / 2
dx, dy = 4.0, 4.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= 8
    if keys[pygame.K_RIGHT]:
        paddle_x += 8
    paddle_x = max(0, min(paddle_x, WIDTH - PADDLE_W))

    # Мяч летит
    bx += dx
    by += dy

    # Отскок: у краёв меняем знак скорости
    if bx < BALL_R or bx > WIDTH - BALL_R:
        dx = -dx                 # развернули влево/вправо
    if by < BALL_R or by > HEIGHT - BALL_R:
        dy = -dy                 # развернули вверх/вниз

    screen.fill(BG)
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, PADDLE_W, PADDLE_H), border_radius=6)
    pygame.draw.circle(screen, BALL_COLOR, (int(bx), int(by)), BALL_R)
    pygame.display.flip()
    clock.tick(60)
