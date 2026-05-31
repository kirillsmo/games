"""
Урок 9: РАДАР. Машина крутит ультразвуковой датчик и шлёт нам "D,угол,см".
Мы рисуем эти точки на экране — как у подводной лодки.

↑↓ ←→ — едем (можно рулить и смотреть радар одновременно)
ESC — выход.

Близкие препятствия — красные, далёкие — зелёные. Луч «прожектора» бежит
туда, куда сейчас смотрит датчик.
"""
import pygame, sys, math
from car_link import connect

car = connect()
car.send("SCAN,1")             # просим машину качать датчиком и слать "D,угол,см"

SPEED = 180
MAX_CM = 100                   # дальше этого не рисуем
R = 240                        # радиус радара в пикселях
CX, CY = 300, 330              # точка машины — внизу по центру, полукруг идёт вверх

command = "S"
beam_angle = 90                # куда сейчас смотрит датчик
blips = []                     # точки на радаре: [угол, см]

pygame.init()
screen = pygame.display.set_mode((600, 360))
pygame.display.set_caption("Робомашинка — радар")
clock = pygame.time.Clock()
small = pygame.font.SysFont(None, 24)


def to_xy(angle, cm):
    """Угол серво (0..180) и расстояние (см) → точка на экране."""
    d = min(cm, MAX_CM) / MAX_CM * R
    x = CX + d * math.cos(math.radians(angle))
    y = CY - d * math.sin(math.radians(angle))
    return int(x), int(y)


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

    # --- читаем телеметрию ---
    line = car.read()
    if line and line.startswith("D,"):
        parts = line.split(",")
        if len(parts) == 3:
            beam_angle = int(parts[1])
            cm = int(parts[2])
            blips.append([beam_angle, cm])
            if len(blips) > 70:           # помним только свежие точки
                blips.pop(0)

    # --- управление ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        drive("F")
    elif keys[pygame.K_DOWN]:
        drive("B")
    elif keys[pygame.K_LEFT]:
        drive("L")
    elif keys[pygame.K_RIGHT]:
        drive("R")
    else:
        drive("S")

    # --- рисуем радар ---
    screen.fill((8, 16, 12))
    for ring in (R, R * 2 // 3, R // 3):       # дуги-кольца дальности
        pygame.draw.arc(screen, (30, 70, 45),
                        (CX - ring, CY - ring, ring * 2, ring * 2), 0, math.pi, 2)
    pygame.draw.line(screen, (30, 70, 45), (CX - R, CY), (CX + R, CY), 2)

    # луч «прожектора»
    bx, by = to_xy(beam_angle, MAX_CM)
    pygame.draw.line(screen, (40, 160, 90), (CX, CY), (bx, by), 2)

    # точки-препятствия
    for a, cm in blips:
        x, y = to_xy(a, cm)
        if cm < 25:
            color = (255, 80, 80)
        elif cm < 55:
            color = (240, 220, 90)
        else:
            color = (90, 220, 120)
        pygame.draw.circle(screen, color, (x, y), 4)

    pygame.draw.circle(screen, (120, 200, 150), (CX, CY), 6)   # сама машина
    info = small.render("Радар · " + str(beam_angle) + "°   (ESC — выход)",
                        True, (150, 200, 170))
    screen.blit(info, (16, 14))
    pygame.display.flip()
    clock.tick(60)
