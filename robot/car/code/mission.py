"""
Урок 11 (проект): «Миссия» — записываем маршрут и машина его повторяет.

Маршрут — это просто список шагов. Каждый шаг — одна команда ("F", "L", "S"...).
Это та же идея «списка объектов», что и в играх (пули, враги, кирпичи).

Управление машиной:  ↑↓ ←→  ·  отпусти — стоп
Кнопки мышкой:
  ЗАПИСАТЬ ШАГ — добавляет текущую команду в маршрут
  ИГРАТЬ       — машина по очереди повторяет все шаги
  ОЧИСТИТЬ     — стирает маршрут
ESC — выход.
"""
import pygame, sys
from car_link import connect

car = connect()
SPEED = 180
STEP_FRAMES = 45               # как долго держим каждый шаг (~0.75 c при 60 FPS)

route = []                     # маршрут — список команд, напр. ["F", "F", "L"]
command = "S"

playing = False
play_index = 0
play_timer = 0

pygame.init()
screen = pygame.display.set_mode((560, 380))
pygame.display.set_caption("Робомашинка — миссия")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
small = pygame.font.SysFont(None, 24)

REC_BTN = pygame.Rect(20, 320, 180, 44)
PLAY_BTN = pygame.Rect(210, 320, 150, 44)
CLR_BTN = pygame.Rect(370, 320, 170, 44)


def send_cmd(cmd):
    """Отправить команду машине (со скоростью, кроме стопа)."""
    car.send("S" if cmd == "S" else cmd + "," + str(SPEED))


def drive(cmd):
    global command
    if cmd != command:
        command = cmd
        send_cmd(cmd)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            car.send("S")
            car.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if REC_BTN.collidepoint(event.pos):
                route.append(command)              # запомнить текущую команду
            elif PLAY_BTN.collidepoint(event.pos) and route:
                playing = True
                play_index = 0
                play_timer = 0
            elif CLR_BTN.collidepoint(event.pos):
                route.clear()
                playing = False

    if playing:
        # повторяем шаги маршрута по очереди
        if play_timer == 0 and play_index < len(route):
            send_cmd(route[play_index])
        play_timer += 1
        if play_timer >= STEP_FRAMES:
            play_timer = 0
            play_index += 1
            if play_index >= len(route):
                playing = False
                send_cmd("S")
                command = "S"
    else:
        # ручное управление
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

    # --- экран ---
    screen.fill((30, 30, 46))
    t1 = font.render("Команда: " + command, True, (22, 196, 127))
    screen.blit(t1, (24, 24))
    t2 = small.render("Маршрут (" + str(len(route)) + " шагов): " + " ".join(route),
                      True, (234, 234, 234))
    screen.blit(t2, (24, 80))
    if playing:
        t3 = small.render("▶ играю шаг " + str(play_index + 1), True, (240, 220, 90))
        screen.blit(t3, (24, 120))
    hint = small.render("↑↓ ←→ — едем · отпусти — стоп", True, (150, 152, 175))
    screen.blit(hint, (24, 170))

    mouse = pygame.mouse.get_pos()
    buttons = [
        (REC_BTN, "Записать шаг", (108, 178, 255)),
        (PLAY_BTN, "Играть", (22, 196, 127)),
        (CLR_BTN, "Очистить", (255, 107, 107)),
    ]
    for rect, label, color in buttons:
        hot = rect.collidepoint(mouse)
        c = color if hot else tuple(int(x * 0.7) for x in color)
        pygame.draw.rect(screen, c, rect, border_radius=8)
        t = small.render(label, True, (12, 14, 30))
        screen.blit(t, t.get_rect(center=rect.center))

    pygame.display.flip()
    clock.tick(60)
