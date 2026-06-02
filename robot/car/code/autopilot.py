"""
Урок 10: автопилот-помощник. Машина едет, но компьютер следит за датчиками
и подстраховывает. РЕШЕНИЕ ПРИНИМАЕТ PYTHON, не Arduino.

• Если впереди ближе 20 см — автотормоз: вперёд ехать нельзя, мигает «СТОП».
• Внизу — три датчика линии (слева/центр/справа): горят, когда видят линию.

↑↓ ←→ — едем · ESC — выход.
"""
import pygame, sys
from robot import connect

car = connect()
car.radar.look(90)             # смотрим прямо по курсу

SPEED = 180
STOP_CM = 20                   # ближе этого вперёд не едем
blink = 0

pygame.init()
screen = pygame.display.set_mode((520, 360))
pygame.display.set_caption("Робомашинка — автопилот")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small = pygame.font.SysFont(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            car.close()
            pygame.quit()
            sys.exit()

    # --- читаем датчики ---
    front_cm = car.radar.measure()         # сколько см до стены прямо по курсу
    line = car.line.read()                 # [слева, центр, справа], 0/1
    blocked = front_cm < STOP_CM

    # --- управление с автотормозом ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not blocked:
        car.forward(SPEED)
    elif keys[pygame.K_DOWN]:
        car.back(SPEED)
    elif keys[pygame.K_LEFT]:
        car.left_turn(SPEED)
    elif keys[pygame.K_RIGHT]:
        car.right_turn(SPEED)
    else:
        car.stop()

    # --- экран ---
    screen.fill((30, 30, 46))
    d = small.render("Впереди: " + str(front_cm) + " см", True, (234, 234, 234))
    screen.blit(d, (24, 30))

    blink = (blink + 1) % 40
    if blocked and blink < 24:
        warn = font.render("⛔ СТОП — СТЕНА!", True, (255, 90, 90))
        screen.blit(warn, (24, 70))

    # датчики линии — три кружка
    labels = ["слева", "центр", "справа"]
    for i in range(3):
        x = 80 + i * 160
        on = line[i] == 1
        color = (22, 196, 127) if on else (70, 70, 90)
        pygame.draw.circle(screen, color, (x, 250), 26)
        t = small.render(labels[i], True, (200, 200, 210))
        screen.blit(t, t.get_rect(center=(x, 300)))

    hint = small.render("↑↓ ←→ · ESC выход", True, (150, 152, 175))
    screen.blit(hint, (24, 330))
    pygame.display.flip()
    clock.tick(60)
