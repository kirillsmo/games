"""
Урок 8: настоящий пульт — плавное управление, скорость и приборная панель.

↑↓ едем · ←→ поворот · отпусти — стоп
+ / -  быстрее / медленнее
ESC — выход.

На экране — «приборы»: команда, скорость (полоской) и состояние связи
(есть машина или режим показа).

Калибровка прямого хода: DC-моторы крутятся чуть по-разному, поэтому машина уводит
в сторону. Подправь trim бортов (см. ниже): тому борту, что быстрее, поставь меньше 1.0.
"""
import pygame, sys
from robot import connect

car = connect()
car.left.trim = 1.0            # ← если уводит вправо — уменьшай left.trim (напр. 0.9)
car.right.trim = 1.0           # ← если уводит влево  — уменьшай right.trim

speed = 180                    # скорость моторов 0..255
command = "стоп"

pygame.init()
screen = pygame.display.set_mode((520, 360))
pygame.display.set_caption("Робомашинка — кокпит")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
small = pygame.font.SysFont(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            car.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                speed = min(255, speed + 20)
            if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                speed = max(80, speed - 20)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.forward(speed);   command = "вперёд"
    elif keys[pygame.K_DOWN]:
        car.back(speed);      command = "назад"
    elif keys[pygame.K_LEFT]:
        car.left_turn(speed); command = "налево"
    elif keys[pygame.K_RIGHT]:
        car.right_turn(speed); command = "направо"
    else:
        car.stop();           command = "стоп"

    # --- приборная панель ---
    screen.fill((30, 30, 46))
    t1 = font.render("Едем: " + command, True, (22, 196, 127))
    screen.blit(t1, (24, 36))

    t2 = small.render("Скорость: " + str(speed), True, (234, 234, 234))
    screen.blit(t2, (24, 110))
    pygame.draw.rect(screen, (60, 60, 80), (24, 140, 255, 20), border_radius=6)
    pygame.draw.rect(screen, (108, 178, 255), (24, 140, speed, 20), border_radius=6)

    link = "есть связь ✅" if car.online else "режим показа 🟡"
    color = (22, 196, 127) if car.online else (240, 200, 80)
    t3 = small.render("Связь: " + link, True, color)
    screen.blit(t3, (24, 190))

    hint = small.render("↑↓ ←→ · +/- скорость · ESC выход", True, (150, 152, 175))
    screen.blit(hint, (24, 300))
    pygame.display.flip()
    clock.tick(60)
