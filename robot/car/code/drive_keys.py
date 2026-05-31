"""
Урок 7: первый заезд — рулим машинкой стрелками по Bluetooth.

↑ вперёд · ↓ назад · ← → поворот · отпусти клавиши — стоп · ESC — выход.

Если машина не подключена, car_link включает «режим показа»: программа
не падает, просто не шлёт команды. Можно пробовать заранее.
"""
import pygame, sys
from car_link import connect

car = connect()
SPEED = 200                    # скорость моторов 0..255

pygame.init()
screen = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Робомашинка — пульт (стрелки)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
small = pygame.font.SysFont(None, 24)

command = "S"                  # какая команда сейчас отправлена


def drive(cmd):
    """Шлём команду только когда она поменялась — не спамим машину."""
    global command
    if cmd != command:
        command = cmd
        if cmd == "S":
            car.send("S")
        else:
            car.send(cmd + "," + str(SPEED))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            car.send("S")
            car.close()
            pygame.quit()
            sys.exit()

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

    screen.fill((30, 30, 46))
    title = font.render("Команда: " + command, True, (22, 196, 127))
    screen.blit(title, (24, 40))
    hint = small.render("↑↓ едем · ←→ поворот · отпусти — стоп · ESC — выход",
                        True, (150, 152, 175))
    screen.blit(hint, (24, 130))
    pygame.display.flip()
    clock.tick(60)
