"""
Урок 7: первый заезд — рулим машинкой стрелками.

↑ вперёд · ↓ назад · ← → поворот · отпусти клавиши — стоп · ESC — выход.

Командуем не «ножками», а понятными объектами: car.forward(), car.left_turn(),
car.stop(). Если машина не подключена, robot.py включает «режим показа»: программа
не падает, просто не шлёт команды. Можно пробовать заранее.
"""
import pygame, sys
from robot import connect

car = connect()
SPEED = 200                    # скорость моторов 0..255

pygame.init()
screen = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Робомашинка — пульт (стрелки)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
small = pygame.font.SysFont(None, 24)

command = "стоп"               # что показываем на экране

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            car.close()
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.forward(SPEED);  command = "вперёд"
    elif keys[pygame.K_DOWN]:
        car.back(SPEED);     command = "назад"
    elif keys[pygame.K_LEFT]:
        car.left_turn(SPEED); command = "налево"
    elif keys[pygame.K_RIGHT]:
        car.right_turn(SPEED); command = "направо"
    else:
        car.stop();          command = "стоп"

    screen.fill((30, 30, 46))
    title = font.render("Едем: " + command, True, (22, 196, 127))
    screen.blit(title, (24, 40))
    hint = small.render("↑↓ едем · ←→ поворот · отпусти — стоп · ESC — выход",
                        True, (150, 152, 175))
    screen.blit(hint, (24, 130))
    pygame.display.flip()
    clock.tick(60)
