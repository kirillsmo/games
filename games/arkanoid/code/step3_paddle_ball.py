"""
Урок 3: мяч отскакивает ОТ РАКЕТКИ, а не от нижней стены.
Новое: colliderect мяча и ракетки, мяч улетел вниз — возвращаем в центр.
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
    paddle = pygame.Rect(paddle_x, paddle_y, PADDLE_W, PADDLE_H)

    bx += dx
    by += dy

    # Теперь нижней стены НЕТ — только левая, правая и верхняя
    if bx < BALL_R or bx > WIDTH - BALL_R:
        dx = -dx
    if by < BALL_R:
        dy = -dy

    ball_rect = pygame.Rect(bx - BALL_R, by - BALL_R, BALL_R * 2, BALL_R * 2)

    # Отскок от ракетки (только если мяч летит вниз)
    if ball_rect.colliderect(paddle) and dy > 0:
        dy = -dy
        # Куда по ракетке попал — туда и уйдёт вбок
        hit = (bx - (paddle_x + PADDLE_W / 2)) / (PADDLE_W / 2)
        dx = 5 * hit

    # Промахнулся — мяч возвращается в центр (пока без штрафа)
    if by > HEIGHT:
        bx, by = WIDTH / 2, HEIGHT / 2
        dx, dy = 4.0, 4.0

    screen.fill(BG)
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, PADDLE_W, PADDLE_H), border_radius=6)
    pygame.draw.circle(screen, BALL_COLOR, (int(bx), int(by)), BALL_R)
    pygame.display.flip()
    clock.tick(60)
