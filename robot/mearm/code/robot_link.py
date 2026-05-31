"""
robot_link.py — связь с роботом по USB.

Открывает порт Arduino и отправляет углы суставов. Если робот не подключён
(или не установлен pyserial) — работает в «режиме показа»: ничего не ломается,
просто не шлёт команды. Так можно писать и пробовать код ещё до сборки.

Использование:
    from robot_link import connect
    robot = connect()        # сам найдёт Arduino
    robot.send(0, 90)        # сустав 0 (база) на 90°
    robot.close()
"""
import glob

BAUD = 9600                      # должно совпадать со скоростью в Arduino


def find_port():
    """Ищем Arduino. Ubuntu: /dev/ttyACM* (Uno) или /dev/ttyUSB* (Nano)."""
    ports = glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*")
    return ports[0] if ports else None


class Robot:
    """Настоящий робот через serial-порт."""

    def __init__(self, port=None, baud=BAUD):
        import serial                       # импортируем тут — чтобы без него тоже работало
        port = port or find_port()
        if port is None:
            raise RuntimeError("Не нашёл Arduino — проверь USB-кабель.")
        self.ser = serial.Serial(port, baud, timeout=1)
        print("✅ Робот подключён:", port)

    def send(self, joint, angle):
        """Отправить угол: joint = 0..3, angle = 0..180."""
        angle = max(0, min(180, int(angle)))
        self.ser.write(f"{joint},{angle}\n".encode())

    def close(self):
        self.ser.close()


class _Offline:
    """Заглушка, когда робота нет: команды просто игнорируются."""

    def send(self, joint, angle):
        pass

    def close(self):
        pass


def connect(port=None):
    """Подключиться к роботу. Нет робота — вернётся «режим показа»."""
    try:
        import serial  # noqa: F401
    except ImportError:
        print("⚠ Нет pyserial (pip install pyserial). Режим показа — без отправки.")
        return _Offline()
    try:
        return Robot(port)
    except Exception as e:
        print("⚠ Робот не подключён — режим показа без отправки:", e)
        return _Offline()
