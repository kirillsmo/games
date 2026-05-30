"""
Диагностика полного экрана. Запусти:  python fullscreen_test.py
В консоли будет видно: ловится ли F и срабатывает ли полный экран.
F — полный экран вкл/выкл, ESC — выход.
"""
import pygame, sys

print("pygame версия:", pygame.ver)
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Тест полного экрана — жми F")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
fullscreen = False

print("Окно создано. Нажимай клавиши — буду печатать их здесь.")

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            print("Нажата клавиша:", pygame.key.name(e.key))
            if e.key == pygame.K_f:
                fullscreen = not fullscreen
                flags = (pygame.SCALED | pygame.FULLSCREEN) if fullscreen else 0
                try:
                    screen = pygame.display.set_mode((600, 400), flags)
                    print("  -> полный экран =", fullscreen, "(OK)")
                except Exception as ex:
                    print("  -> ОШИБКА:", type(ex).__name__, ex)
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill((30, 30, 46))
    pygame.draw.circle(screen, (22, 196, 127), (300, 200), 50)
    text = font.render("F — полный экран, ESC — выход", True, (234, 234, 234))
    screen.blit(text, text.get_rect(center=(300, 320)))
    pygame.display.flip()
    clock.tick(60)
