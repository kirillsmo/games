"""
Арканоид — отбивай мяч ракеткой и ломай кирпичи!
Стрелки влево/вправо — двигать ракетку. Пробел — играть заново.
F — полный экран, ESC — выход.
"""
import pygame, sys

WIDTH, HEIGHT = 600, 400
BG = (30, 30, 46)
WHITE = (234, 234, 234)
GREEN = (22, 196, 127)
RED = (255, 107, 107)
BALL_COLOR = (255, 209, 102)
BRICK_COLORS = [(255, 107, 107), (255, 165, 89), (255, 209, 102),
                (106, 205, 140), (108, 178, 255)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
fullscreen = False
pygame.display.set_caption("Арканоид")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 56)

PADDLE_W, PADDLE_H = 90, 14
paddle_y = HEIGHT - 30
BALL_R = 8

COLS, ROWS = 10, 5
BRICK_W = WIDTH // COLS
BRICK_H = 24
GAP = 3
TOP = 40            # отступ кирпичей сверху


def make_bricks():
    """Список прямоугольников-кирпичей: ROWS строк по COLS штук."""
    bricks = []
    for row in range(ROWS):
        for col in range(COLS):
            x = col * BRICK_W + GAP
            y = TOP + row * BRICK_H + GAP
            bricks.append(pygame.Rect(x, y, BRICK_W - GAP * 2, BRICK_H - GAP * 2))
    return bricks


def new_game():
    paddle_x = WIDTH // 2 - PADDLE_W // 2
    bx, by = WIDTH / 2, HEIGHT / 2     # мяч по центру
    dx, dy = 4.0, 4.0                  # скорость мяча
    return paddle_x, bx, by, dx, dy, make_bricks(), 0, 3


paddle_x, bx, by, dx, dy, bricks, score, lives = new_game()
state = "play"        # "play" | "over" | "win"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:                 # F — полный экран вкл/выкл
                fullscreen = not fullscreen
                flags = pygame.SCALED | (pygame.FULLSCREEN if fullscreen else 0)
                screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN and state != "play" and event.key == pygame.K_SPACE:
            paddle_x, bx, by, dx, dy, bricks, score, lives = new_game()
            state = "play"

    if state == "play":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x -= 8
        if keys[pygame.K_RIGHT]:
            paddle_x += 8
        paddle_x = max(0, min(paddle_x, WIDTH - PADDLE_W))
        paddle = pygame.Rect(paddle_x, paddle_y, PADDLE_W, PADDLE_H)

        # Мяч летит
        bx += dx
        by += dy

        # Отскок от стен: левая/правая меняют dx, верхняя меняет dy
        if bx < BALL_R or bx > WIDTH - BALL_R:
            dx = -dx
        if by < BALL_R:
            dy = -dy

        ball_rect = pygame.Rect(bx - BALL_R, by - BALL_R, BALL_R * 2, BALL_R * 2)

        # Отскок от ракетки (только когда мяч летит вниз)
        if ball_rect.colliderect(paddle) and dy > 0:
            dy = -dy
            # Куда по ракетке попал — туда и уйдёт вбок
            hit = (bx - (paddle_x + PADDLE_W / 2)) / (PADDLE_W / 2)
            dx = 5 * hit

        # Кирпичи: попали — убираем кирпич и отскакиваем
        for brick in bricks:
            if ball_rect.colliderect(brick):
                bricks.remove(brick)
                dy = -dy
                score += 1
                break

        # Мяч упал ниже экрана — минус жизнь
        if by > HEIGHT:
            lives -= 1
            bx, by = WIDTH / 2, HEIGHT / 2
            dx, dy = 4.0, 4.0
            if lives <= 0:
                state = "over"

        # Все кирпичи разбиты — победа
        if not bricks:
            state = "win"

    # Рисуем
    screen.fill(BG)
    for brick in bricks:
        row = (brick.y - TOP) // BRICK_H
        pygame.draw.rect(screen, BRICK_COLORS[row % len(BRICK_COLORS)], brick)
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, PADDLE_W, PADDLE_H), border_radius=6)
    pygame.draw.circle(screen, BALL_COLOR, (int(bx), int(by)), BALL_R)
    hud = font.render(f"Очки: {score}    Жизни: {lives}", True, WHITE)
    screen.blit(hud, (12, 8))

    if state != "play":
        msg = "Победа!" if state == "win" else "Игра окончена"
        color = GREEN if state == "win" else RED
        t1 = big_font.render(msg, True, color)
        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        t2 = font.render("Пробел — играть заново", True, WHITE)
        screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

    pygame.display.flip()
    clock.tick(60)
