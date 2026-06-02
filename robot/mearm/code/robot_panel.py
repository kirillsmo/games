"""
Урок 10: пульт робота + запись и воспроизведение поз.

Управление суставами — как в уроке 9 (← → ↑ ↓ W S O C).
Кнопки мышкой:
  ЗАПИСАТЬ ПОЗУ — добавляет текущие углы в список поз
  ИГРАТЬ        — робот по очереди повторяет все записанные позы
  ОЧИСТИТЬ      — стирает список
ESC — выход.

Поза — это просто список из 4 углов. Программа робота — список поз.
Это та же идея «списка объектов», что и в играх (пули, враги, кирпичи).
"""
import pygame, sys
from arm import connect

arm = connect()
poses = []                       # список записанных поз (каждая — [a0,a1,a2,a3])

playing = False
play_index = 0
play_timer = 0
PLAY_DELAY = 45                  # кадров между позами (~0.75 c при 60 FPS)
STEP = 2

pygame.init()
screen = pygame.display.set_mode((520, 380))
pygame.display.set_caption("Робот — пульт и запись поз")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
small = pygame.font.SysFont(None, 22)

REC_BTN = pygame.Rect(20, 300, 160, 40)
PLAY_BTN = pygame.Rect(190, 300, 150, 40)
CLR_BTN = pygame.Rect(350, 300, 150, 40)


def move(joint, delta):
    arm.joints[joint].angle += delta


def apply_pose(pose):
    for j in range(4):
        arm.set(j, pose[j])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            arm.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if REC_BTN.collidepoint(event.pos):
                poses.append(arm.angles())          # запомнить текущую позу
            elif PLAY_BTN.collidepoint(event.pos) and poses:
                playing = True
                play_index = 0
                play_timer = 0
            elif CLR_BTN.collidepoint(event.pos):
                poses.clear()
                playing = False

    if playing:
        # Проигрываем позы по очереди
        if play_timer == 0 and play_index < len(poses):
            apply_pose(poses[play_index])
        play_timer += 1
        if play_timer >= PLAY_DELAY:
            play_timer = 0
            play_index += 1
            if play_index >= len(poses):
                playing = False
    else:
        # Ручное управление с клавиатуры
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  move(0, -STEP)
        if keys[pygame.K_RIGHT]: move(0, +STEP)
        if keys[pygame.K_UP]:    move(1, +STEP)
        if keys[pygame.K_DOWN]:  move(1, -STEP)
        if keys[pygame.K_w]:     move(2, +STEP)
        if keys[pygame.K_s]:     move(2, -STEP)
        if keys[pygame.K_o]:     move(3, +STEP)
        if keys[pygame.K_c]:     move(3, -STEP)

    # Рисуем
    screen.fill((30, 30, 46))
    for i, s in enumerate(arm.joints):
        line = font.render(f"{s.name}: {s.angle}°", True, (22, 196, 127))
        screen.blit(line, (24, 20 + i * 34))
    info = small.render(f"Записано поз: {len(poses)}" + ("   ▶ играю..." if playing else ""),
                        True, (234, 234, 234))
    screen.blit(info, (24, 168))
    hint = small.render("← → база · ↑ ↓ плечо · W S локоть · O C захват", True, (150, 152, 175))
    screen.blit(hint, (24, 210))

    mouse = pygame.mouse.get_pos()
    for rect, label, color in [
        (REC_BTN, "Записать позу", (108, 178, 255)),
        (PLAY_BTN, "Играть", (22, 196, 127)),
        (CLR_BTN, "Очистить", (255, 107, 107)),
    ]:
        hot = rect.collidepoint(mouse)
        c = color if hot else tuple(int(x * 0.7) for x in color)
        pygame.draw.rect(screen, c, rect, border_radius=8)
        t = small.render(label, True, (12, 14, 30))
        screen.blit(t, t.get_rect(center=rect.center))

    pygame.display.flip()
    clock.tick(60)
