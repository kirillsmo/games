"""
Урок 9: РАДАР. Python сам качает датчик и меряет расстояние — как у подлодки.

Каждый кадр мы поворачиваем серво на новый угол (car.radar.look) и меряем
расстояние (car.radar.measure). Точки рисуем на экране: близкие — красные,
далёкие — зелёные. Луч «прожектора» бежит туда, куда сейчас смотрит датчик.

↑↓ ←→ — едем (можно рулить и смотреть радар одновременно)
ESC — выход.
"""
import pygame, sys, math
from robot import connect

car = connect()

SPEED = 180
MAX_CM = 100                   # дальше этого не рисуем
R = 240                        # радиус радара в пикселях
CX, CY = 300, 330              # точка машины — внизу по центру, полукруг идёт вверх

beam_angle = 90                # куда сейчас смотрит датчик
sweep_dir = 6                  # шаг качания (туда-сюда)
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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            car.close()
            pygame.quit()
            sys.exit()

    # --- качаем датчик и меряем (это делает Python, не Arduino) ---
    car.radar.look(beam_angle)
    cm = car.radar.measure()
    blips.append([beam_angle, cm])
    if len(blips) > 70:                   # помним только свежие точки
        blips.pop(0)
    beam_angle += sweep_dir
    if beam_angle >= 174 or beam_angle <= 6:
        sweep_dir = -sweep_dir

    # --- управление ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.forward(SPEED)
    elif keys[pygame.K_DOWN]:
        car.back(SPEED)
    elif keys[pygame.K_LEFT]:
        car.left_turn(SPEED)
    elif keys[pygame.K_RIGHT]:
        car.right_turn(SPEED)
    else:
        car.stop()

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
