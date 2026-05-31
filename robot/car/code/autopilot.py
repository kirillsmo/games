"""
Урок 10: автопилот-помощник. Машина едет, но компьютер следит за датчиками
и подстраховывает.

• Если впереди ближе 20 см — автотормоз: вперёд ехать нельзя, мигает «СТОП».
• Внизу — три датчика линии (слева/середина/справа): горят, когда видят линию.

↑↓ ←→ — едем · ESC — выход.
"""
import pygame, sys
from car_link import connect

car = connect()
car.send("SCAN,1")             # пусть качает датчиком и шлёт расстояние

SPEED = 180
STOP_CM = 20                   # ближе этого вперёд не едем
front_cm = 100                 # что видим прямо по курсу
line = [0, 0, 0]               # датчики линии: слева, середина, справа
command = "S"
blink = 0

pygame.init()
screen = pygame.display.set_mode((520, 360))
pygame.display.set_caption("Робомашинка — автопилот")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small = pygame.font.SysFont(None, 24)


def drive(cmd):
    global command
    if cmd != command:
        command = cmd
        car.send("S" if cmd == "S" else cmd + "," + str(SPEED))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            car.send("S")
            car.send("SCAN,0")
            car.close()
            pygame.quit()
            sys.exit()

    # --- телеметрия ---
    msg = car.read()
    if msg and msg.startswith("D,"):
        parts = msg.split(",")
        if len(parts) == 3 and 70 <= int(parts[1]) <= 110:   # смотрим прямо по курсу
            front_cm = int(parts[2])
    if msg and msg.startswith("T,"):
        parts = msg.split(",")
        if len(parts) == 4:
            line = [int(parts[1]), int(parts[2]), int(parts[3])]

    blocked = front_cm < STOP_CM

    # --- управление с автотормозом ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not blocked:
        drive("F")
    elif keys[pygame.K_DOWN]:
        drive("B")
    elif keys[pygame.K_LEFT]:
        drive("L")
    elif keys[pygame.K_RIGHT]:
        drive("R")
    else:
        drive("S")

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
