"""
Урок 8: двигаем ОДИН сустав робота с клавиатуры.
Стрелки влево/вправо — поворачивают базу. ESC — выход.

Это тот же игровой цикл pygame, что и в играх, только вместо рисованного
объекта мы двигаем настоящий сустав робота — объект arm.base.
"""
import pygame, sys
from arm import connect

arm = connect()                   # найдёт Arduino (Firmata) или включит «режим показа»

pygame.init()
screen = pygame.display.set_mode((520, 220))
pygame.display.set_caption("Робот — поворот базы")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            arm.close()
            pygame.quit()
            sys.exit()

    # Зажатые стрелки плавно крутят базу. Пределы 0..180 объект хранит сам.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        arm.base.angle -= 2
    if keys[pygame.K_RIGHT]:
        arm.base.angle += 2

    screen.fill((30, 30, 46))
    text = font.render(f"База: {arm.base.angle}°", True, (234, 234, 234))
    screen.blit(text, text.get_rect(center=(260, 90)))
    hint = pygame.font.SysFont(None, 26).render("← →  крутить · ESC выход", True, (150, 152, 175))
    screen.blit(hint, hint.get_rect(center=(260, 150)))
    pygame.display.flip()
    clock.tick(60)
