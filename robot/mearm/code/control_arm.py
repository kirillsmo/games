"""
Урок 9: управляем ВСЕМИ 4 суставами робота с клавиатуры.

  База (поворот):  ←  →
  Плечо:           ↑  ↓
  Локоть:          W  S
  Захват:          O (открыть)  C (закрыть)
  ESC — выход.

На экране видно текущие углы. У каждого сустава свои безопасные пределы,
чтобы не сломать механику (как и в прошивке Arduino).
"""
import pygame, sys
from robot_link import connect

robot = connect()

# Имя сустава и его пределы (мин, макс). Подбери под свою сборку!
JOINTS = [
    {"name": "База",   "lo": 0,  "hi": 180},
    {"name": "Плечо",  "lo": 30, "hi": 150},
    {"name": "Локоть", "lo": 30, "hi": 150},
    {"name": "Захват", "lo": 20, "hi": 120},
]
angles = [90, 90, 90, 60]         # стартовые углы

pygame.init()
screen = pygame.display.set_mode((460, 320))
pygame.display.set_caption("Робот — управление рукой")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
small = pygame.font.SysFont(None, 24)

STEP = 2                          # на сколько градусов за кадр


def move(joint, delta):
    lo, hi = JOINTS[joint]["lo"], JOINTS[joint]["hi"]
    angles[joint] = max(lo, min(hi, angles[joint] + delta))
    robot.send(joint, angles[joint])


for j in range(4):                # выставить старт на роботе
    robot.send(j, angles[j])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            robot.close()
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  move(0, -STEP)
    if keys[pygame.K_RIGHT]: move(0, +STEP)
    if keys[pygame.K_UP]:    move(1, +STEP)
    if keys[pygame.K_DOWN]:  move(1, -STEP)
    if keys[pygame.K_w]:     move(2, +STEP)
    if keys[pygame.K_s]:     move(2, -STEP)
    if keys[pygame.K_o]:     move(3, +STEP)   # открыть
    if keys[pygame.K_c]:     move(3, -STEP)   # закрыть

    # Рисуем углы суставов
    screen.fill((30, 30, 46))
    title = font.render("Углы суставов", True, (234, 234, 234))
    screen.blit(title, (20, 16))
    for i, j in enumerate(JOINTS):
        line = font.render(f"{j['name']}: {angles[i]}°", True, (22, 196, 127))
        screen.blit(line, (30, 60 + i * 42))
    hint = small.render("← → база · ↑ ↓ плечо · W S локоть · O C захват · ESC", True, (150, 152, 175))
    screen.blit(hint, (16, 286))
    pygame.display.flip()
    clock.tick(60)
