"""
Урок 1: ракетка ездит внизу.
Повторяем из «Ловкого кота»: движение в пикселях, pygame.key.get_pressed().
"""
import pygame, sys

WIDTH, HEIGHT = 600, 400
BG = (30, 30, 46)
GREEN = (22, 196, 127)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")
clock = pygame.time.Clock()

PADDLE_W, PADDLE_H = 90, 14
paddle_x = WIDTH // 2 - PADDLE_W // 2
paddle_y = HEIGHT - 30

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

    screen.fill(BG)
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, PADDLE_W, PADDLE_H), border_radius=6)
    pygame.display.flip()
    clock.tick(60)
