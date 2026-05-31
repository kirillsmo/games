"""
Урок 12 (бонус): FPV — «вид от первого лица» с камеры ESP32-CAM.

Камера ESP32-CAM раздаёт видео по Wi-Fi: это поток картинок-JPEG (формат MJPEG)
по адресу вроде http://192.168.4.1:81/stream . Мы читаем поток, вырезаем из него
кадры и показываем в pygame — получается видео с машины.

ВАЖНО (продвинутый урок):
  • Узнай IP-адрес камеры (его печатает ESP32-CAM в Serial Monitor) и впиши в CAM_URL.
  • Подключи ноутбук к Wi-Fi камеры.
  • Если камеры нет — программа покажет заставку «нет сигнала», но не упадёт.

ESC — выход.
"""
import pygame, sys, io, threading
import urllib.request

CAM_URL = "http://192.168.4.1:81/stream"     # ← впиши адрес своей камеры

latest_jpeg = None             # последний пойманный кадр (байты JPEG)
running = True


def reader():
    """Фоновый поток: читает MJPEG и складывает последний кадр в latest_jpeg."""
    global latest_jpeg
    try:
        stream = urllib.request.urlopen(CAM_URL, timeout=5)
    except Exception as e:
        print("⚠ Камера не найдена:", e)
        return
    buf = b""
    while running:
        buf += stream.read(1024)
        start = buf.find(b"\xff\xd8")          # начало JPEG
        end = buf.find(b"\xff\xd9")            # конец JPEG
        if start != -1 and end != -1 and end > start:
            latest_jpeg = buf[start:end + 2]
            buf = buf[end + 2:]


threading.Thread(target=reader, daemon=True).start()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Робомашинка — FPV камера")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False
            pygame.quit()
            sys.exit()

    screen.fill((10, 10, 16))
    if latest_jpeg:
        try:
            frame = pygame.image.load(io.BytesIO(latest_jpeg))
            frame = pygame.transform.scale(frame, (640, 480))
            screen.blit(frame, (0, 0))
        except Exception:
            pass
    else:
        msg = font.render("📷 нет сигнала с камеры...", True, (200, 200, 210))
        screen.blit(msg, msg.get_rect(center=(320, 240)))

    pygame.display.flip()
    clock.tick(30)
