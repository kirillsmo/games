"""
Урок 9: управляем ВСЕМИ 4 суставами робота с клавиатуры.

  База (поворот):  ←  →
  Плечо:           ↑  ↓
  Локоть:          W  S
  Захват:          O (открыть)  C (закрыть)
  ESC — выход.

На экране видно текущие углы. Безопасные пределы каждого сустава хранит сам объект
Servo (см. LIMITS в arm.py) — за них не выйти, механику не сломать.
"""
import pygame, sys
from arm import connect

arm = connect()
STEP = 2                          # на сколько градусов за кадр


def move(joint, delta):
    """Подвинуть сустав. Объект сам обрежет угол по пределам."""
    arm.joints[joint].angle += delta


pygame.init()
screen = pygame.display.set_mode((460, 320))
pygame.display.set_caption("Робот — управление рукой")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 34)
small = pygame.font.SysFont(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            arm.close()
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
    for i, s in enumerate(arm.joints):
        line = font.render(f"{s.name}: {s.angle}°", True, (22, 196, 127))
        screen.blit(line, (30, 60 + i * 42))
    hint = small.render("← → база · ↑ ↓ плечо · W S локоть · O C захват · ESC", True, (150, 152, 175))
    screen.blit(hint, (16, 286))
    pygame.display.flip()
    clock.tick(60)
