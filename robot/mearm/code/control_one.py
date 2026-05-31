"""
Урок 8: двигаем ОДИН сустав робота с клавиатуры.
Стрелки влево/вправо — поворачивают базу (сустав 0). ESC — выход.

Это тот же игровой цикл pygame, что и в играх, только вместо рисованного
объекта мы шлём угол настоящему роботу по USB.
"""
import pygame, sys
from robot_link import connect

robot = connect()                 # найдёт Arduino или включит «режим показа»

pygame.init()
screen = pygame.display.set_mode((520, 220))
pygame.display.set_caption("Робот — поворот базы")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

angle = 90                        # текущий угол базы
robot.send(0, angle)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            robot.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            robot.close()
            pygame.quit()
            sys.exit()

    # Зажатые стрелки плавно крутят базу
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle -= 2
    if keys[pygame.K_RIGHT]:
        angle += 2
    angle = max(0, min(180, angle))   # не выходим за 0..180
    robot.send(0, angle)              # отправляем угол роботу

    screen.fill((30, 30, 46))
    text = font.render(f"База: {angle}°", True, (234, 234, 234))
    screen.blit(text, text.get_rect(center=(260, 90)))
    hint = pygame.font.SysFont(None, 26).render("← →  крутить · ESC выход", True, (150, 152, 175))
    screen.blit(hint, hint.get_rect(center=(260, 150)))
    pygame.display.flip()
    clock.tick(60)
