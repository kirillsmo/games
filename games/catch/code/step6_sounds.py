"""
Ловкий кот — лови падающие яблоки!
Стрелки влево/вправо — двигать кота. Пробел — заново после проигрыша.
F — полный экран, ESC — выход.
"""
import pygame, sys, random, os

WIDTH, HEIGHT = 600, 400
HERE = os.path.dirname(__file__)   # папка, где лежит этот файл

BG = (30, 30, 46)
WHITE = (234, 234, 234)
RED = (255, 107, 107)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Ловкий кот")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# Картинки (assets лежат рядом с этим файлом)
cat_img = pygame.image.load(os.path.join(HERE, "assets", "cat.png")).convert_alpha()
apple_img = pygame.image.load(os.path.join(HERE, "assets", "apple.png")).convert_alpha()
cat_w, cat_h = cat_img.get_size()
apple_w, apple_h = apple_img.get_size()
cat_y = HEIGHT - cat_h - 10

# Звуки
catch_sound = pygame.mixer.Sound(os.path.join(HERE, "assets", "catch.wav"))
miss_sound = pygame.mixer.Sound(os.path.join(HERE, "assets", "miss.wav"))


def new_apple():
    """Новое яблоко: случайно по горизонтали, чуть выше экрана."""
    return random.randint(0, WIDTH - apple_w), -apple_h


def new_game():
    cat_x = WIDTH // 2 - cat_w // 2
    apple_x, apple_y = new_apple()
    return cat_x, apple_x, apple_y, 0, 3, 4.0   # cat_x, apple_x, apple_y, score, lives, speed


cat_x, apple_x, apple_y, score, lives, speed = new_game()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()   # F — полный экран
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_SPACE:
            cat_x, apple_x, apple_y, score, lives, speed = new_game()
            game_over = False

    if not game_over:
        # Зажатые клавиши — плавное движение
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cat_x -= 7
        if keys[pygame.K_RIGHT]:
            cat_x += 7
        # Не выпускаем кота за края
        cat_x = max(0, min(cat_x, WIDTH - cat_w))

        # Яблоко падает
        apple_y += speed

        cat_rect = pygame.Rect(cat_x, cat_y, cat_w, cat_h)
        apple_rect = pygame.Rect(apple_x, apple_y, apple_w, apple_h)

        if cat_rect.colliderect(apple_rect):
            score += 1
            speed += 0.3                 # с каждым яблоком чуть быстрее
            catch_sound.play()
            apple_x, apple_y = new_apple()
        elif apple_y > HEIGHT:
            lives -= 1
            miss_sound.play()
            apple_x, apple_y = new_apple()
            if lives <= 0:
                game_over = True

    # Рисуем
    screen.fill(BG)
    screen.blit(apple_img, (apple_x, apple_y))
    screen.blit(cat_img, (cat_x, cat_y))
    hud = font.render(f"Очки: {score}    Жизни: {lives}", True, WHITE)
    screen.blit(hud, (12, 10))

    if game_over:
        t1 = big_font.render("Игра окончена!", True, RED)
        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        t2 = font.render("Пробел — играть заново", True, WHITE)
        screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    pygame.display.flip()
    clock.tick(60)
