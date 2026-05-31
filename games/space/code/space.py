"""
Космос — стреляй по падающим пришельцам!
Стрелки влево/вправо — двигать корабль. Пробел — стрелять.
Когда игра окончена — кнопка на экране или Enter запускают заново.
F — полный экран, ESC — выход.
"""
import pygame, sys, random, os

WIDTH, HEIGHT = 600, 400
BG = (15, 16, 38)
WHITE = (234, 234, 234)
GREEN = (22, 196, 127)
RED = (255, 107, 107)
SHIP_COLOR = (108, 178, 255)
BULLET_COLOR = (255, 209, 102)
ENEMY_COLOR = (255, 107, 107)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fullscreen = False
pygame.display.set_caption("Космос")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 56)

# Звуки. Если папки assets нет — игра работает без звука (молча).
HERE = os.path.dirname(__file__)
class _Silent:
    def play(self):
        pass
try:
    pygame.mixer.init()
    def _snd(name):
        return pygame.mixer.Sound(os.path.join(HERE, "assets", name))
    shoot_sound = _snd("shoot.wav")
    boom_sound = _snd("boom.wav")
    hit_sound = _snd("hit.wav")
    gameover_sound = _snd("gameover.wav")
except Exception:
    shoot_sound = boom_sound = hit_sound = gameover_sound = _Silent()

# Фоновая музыка (тоже необязательная — без файла просто не играет)
try:
    pygame.mixer.music.load(os.path.join(HERE, "assets", "music.wav"))
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)          # -1 = повторять бесконечно
except Exception:
    pass

SHIP_W, SHIP_H = 40, 28
ship_y = HEIGHT - SHIP_H - 12      # корабль внизу
SHIP_SPEED = 6

BULLET_W, BULLET_H = 4, 14
BULLET_SPEED = 9

ENEMY_SIZE = 32
ENEMY_SPEED = 2
SPAWN_EVERY = 45                   # через сколько кадров появляется новый враг

# Звёзды на фоне (просто для красоты)
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(40)]

small_font = pygame.font.SysFont(None, 26)

# Кнопки на экране «Игра окончена» (прямоугольники, по ним кликаем мышкой)
RESTART_BTN = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 24, 240, 46)
QUIT_BTN = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 82, 160, 36)


def draw_ship(x):
    """Корабль — синий треугольник носом вверх."""
    points = [(x, ship_y), (x - SHIP_W // 2, ship_y + SHIP_H), (x + SHIP_W // 2, ship_y + SHIP_H)]
    pygame.draw.polygon(screen, SHIP_COLOR, points)
    pygame.draw.circle(screen, WHITE, (x, ship_y + SHIP_H - 8), 4)


def draw_enemy(e):
    """Пришелец — красный кружок с глазками."""
    ex, ey = e.center
    pygame.draw.circle(screen, ENEMY_COLOR, (ex, ey), ENEMY_SIZE // 2)
    pygame.draw.circle(screen, WHITE, (ex - 6, ey - 3), 4)
    pygame.draw.circle(screen, WHITE, (ex + 6, ey - 3), 4)
    pygame.draw.circle(screen, BG, (ex - 6, ey - 3), 2)
    pygame.draw.circle(screen, BG, (ex + 6, ey - 3), 2)


def new_game():
    ship_x = WIDTH // 2
    bullets = []          # список пуль
    enemies = []          # список врагов
    return ship_x, bullets, enemies, 0, 3, 0


ship_x, bullets, enemies, score, lives, spawn_timer = new_game()
state = "play"            # "play" | "over"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:                 # F — полный экран вкл/выкл
                fullscreen = not fullscreen
                flags = (pygame.SCALED | pygame.FULLSCREEN) if fullscreen else 0
                screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE and state == "play":
                # выстрел — добавляем новую пулю в список (пробел больше НЕ перезапускает!)
                bullets.append(pygame.Rect(ship_x - BULLET_W // 2, ship_y, BULLET_W, BULLET_H))
                shoot_sound.play()
            elif event.key == pygame.K_RETURN and state == "over":
                ship_x, bullets, enemies, score, lives, spawn_timer = new_game()
                state = "play"
        # На экране «Игра окончена» — клик мышкой по кнопкам
        if event.type == pygame.MOUSEBUTTONDOWN and state == "over":
            if RESTART_BTN.collidepoint(event.pos):
                ship_x, bullets, enemies, score, lives, spawn_timer = new_game()
                state = "play"
            elif QUIT_BTN.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    if state == "play":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship_x -= SHIP_SPEED
        if keys[pygame.K_RIGHT]:
            ship_x += SHIP_SPEED
        ship_x = max(SHIP_W // 2, min(ship_x, WIDTH - SHIP_W // 2))
        ship_rect = pygame.Rect(ship_x - SHIP_W // 2, ship_y, SHIP_W, SHIP_H)

        # Пули летят вверх; улетевшие за экран убираем из списка
        for b in bullets[:]:
            b.y -= BULLET_SPEED
            if b.bottom < 0:
                bullets.remove(b)

        # Появляются новые враги
        spawn_timer += 1
        if spawn_timer >= SPAWN_EVERY:
            spawn_timer = 0
            x = random.randint(0, WIDTH - ENEMY_SIZE)
            enemies.append(pygame.Rect(x, -ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE))

        # Враги летят вниз
        for e in enemies[:]:
            e.y += ENEMY_SPEED
            if e.top > HEIGHT:                  # прорвался вниз — минус жизнь
                enemies.remove(e)
                lives -= 1
                hit_sound.play()
            elif e.colliderect(ship_rect):      # врезался в корабль — минус жизнь
                enemies.remove(e)
                lives -= 1
                hit_sound.play()

        # Попадания: пуля встретила врага — убираем обоих, +1 очко
        for b in bullets[:]:
            for e in enemies[:]:
                if b.colliderect(e):
                    bullets.remove(b)
                    enemies.remove(e)
                    score += 1
                    boom_sound.play()
                    break

        if lives <= 0:
            state = "over"
            gameover_sound.play()

    # Рисуем
    screen.fill(BG)
    for sx, sy in stars:
        screen.set_at((sx, sy), (90, 92, 120))
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b)
    for e in enemies:
        draw_enemy(e)
    draw_ship(ship_x)
    hud = font.render(f"Очки: {score}    Жизни: {lives}", True, WHITE)
    screen.blit(hud, (12, 8))

    if state == "over":
        # Затемняем поле, чтобы экран был хорошо виден
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill((10, 10, 25))
        screen.blit(overlay, (0, 0))

        t1 = big_font.render("Игра окончена", True, RED)
        screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))
        sc = font.render(f"Твой счёт: {score}", True, WHITE)
        screen.blit(sc, sc.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))

        mouse = pygame.mouse.get_pos()
        # Кнопка «Играть заново» (подсвечивается при наведении)
        hot = RESTART_BTN.collidepoint(mouse)
        pygame.draw.rect(screen, GREEN if hot else (18, 150, 100), RESTART_BTN, border_radius=10)
        bt = font.render("Играть заново", True, (6, 40, 26))
        screen.blit(bt, bt.get_rect(center=RESTART_BTN.center))
        # Кнопка «Выход»
        hotq = QUIT_BTN.collidepoint(mouse)
        pygame.draw.rect(screen, (70, 72, 95) if hotq else (45, 46, 64), QUIT_BTN, border_radius=8)
        qt = font.render("Выход", True, WHITE)
        screen.blit(qt, qt.get_rect(center=QUIT_BTN.center))

        hint = small_font.render("Enter — заново · Esc — выход", True, (150, 152, 175))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 132)))

    pygame.display.flip()
    clock.tick(60)
