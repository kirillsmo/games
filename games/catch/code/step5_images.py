"""
Урок 5: настоящие картинки вместо прямоугольников.
Новое: pygame.image.load, .convert_alpha(), screen.blit(), пути к файлам через os.
Нужна папка assets рядом с этим файлом (cat.png, apple.png).
"""
import pygame, sys, random, os

WIDTH, HEIGHT = 600, 400
HERE = os.path.dirname(__file__)   # папка, где лежит этот файл
BG = (30, 30, 46)
WHITE = (234, 234, 234)
PINK = (255, 107, 107)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловкий кот")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# Загружаем картинки. convert_alpha() — чтобы прозрачные углы были прозрачными.
cat_img = pygame.image.load(os.path.join(HERE, "assets", "cat.png")).convert_alpha()
apple_img = pygame.image.load(os.path.join(HERE, "assets", "apple.png")).convert_alpha()
cat_w, cat_h = cat_img.get_size()
apple_w, apple_h = apple_img.get_size()
cat_y = HEIGHT - cat_h - 10


def new_game():
    cat_x = WIDTH // 2 - cat_w // 2
    apple_x = random.randint(0, WIDTH - apple_w)
    return cat_x, apple_x, -apple_h, 0, 3, 4.0


cat_x, apple_x, apple_y, score, lives, speed = new_game()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_SPACE:
            cat_x, apple_x, apple_y, score, lives, speed = new_game()
            game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cat_x -= 7
        if keys[pygame.K_RIGHT]:
            cat_x += 7
        cat_x = max(0, min(cat_x, WIDTH - cat_w))

        apple_y += speed
        cat_rect = pygame.Rect(cat_x, cat_y, cat_w, cat_h)
        apple_rect = pygame.Rect(apple_x, apple_y, apple_w, apple_h)

        if cat_rect.colliderect(apple_rect):
            score += 1
            speed += 0.3
            apple_x = random.randint(0, WIDTH - apple_w)
            apple_y = -apple_h
        elif apple_y > HEIGHT:
            lives -= 1
            apple_x = random.randint(0, WIDTH - apple_w)
            apple_y = -apple_h
            if lives <= 0:
                game_over = True

    screen.fill(BG)
    # blit — «приклеить» картинку на экран в точку (x, y)
    screen.blit(apple_img, (apple_x, apple_y))
    screen.blit(cat_img, (cat_x, cat_y))
    hud = font.render(f"Очки: {score}    Жизни: {lives}", True, WHITE)
    screen.blit(hud, (12, 10))
    if game_over:
        t1 = big_font.render("Игра окончена!", True, PINK)
        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        t2 = font.render("Пробел — играть заново", True, WHITE)
        screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()
    clock.tick(60)
