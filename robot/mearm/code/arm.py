"""
arm.py — управление рукой MeArm из Python через Firmata.

Никакого своего протокола! Один раз заливаем в Arduino стандартную прошивку
FirmataExpress (см. arduino/README.txt). После этого плата просто слушается
компьютера, а весь «ум» робота живёт в Python. Библиотека pymata4 сама управляет
ножками, а мы прячем её за понятными объектами-суставами.

4 сервопривода подключены прямо к ножкам Arduino Nano:
    база = 9, плечо = 10, локоть = 11, захват = 6
(поменяй номера под свою сборку — см. урок 6).

Использование:
    from arm import connect
    arm = connect()
    arm.base.angle = 120        # повернуть базу на 120°
    arm.set(0, 90)              # то же самое по номеру сустава
    arm.close()

Нет робота (или не установлен pymata4) — включается «режим показа»: код не падает,
просто никуда не шлёт. Так можно писать программу ещё до сборки.

Установка библиотеки:  pip install pymata4
"""

SERVO_PINS = [9, 10, 11, 6]               # база, плечо, локоть, захват
NAMES = ["база", "плечо", "локоть", "захват"]
# Безопасные пределы углов для каждого сустава (подбери под свою сборку!)
LIMITS = [(0, 180), (30, 150), (30, 150), (20, 120)]
START = [90, 90, 90, 60]                  # стартовые углы (центр)


class Servo:
    """Один сустав-сервопривод. У него есть угол с безопасными пределами."""

    def __init__(self, board, pin, lo, hi, name):
        self.board = board                # объект pymata4 или None в режиме показа
        self.pin = pin
        self.lo, self.hi = lo, hi
        self.name = name
        self._angle = 90
        if board is not None:
            board.set_pin_mode_servo(pin)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        value = max(self.lo, min(self.hi, int(value)))   # не выходим за пределы
        self._angle = value
        if self.board is not None:
            self.board.servo_write(self.pin, value)


class Arm:
    """Вся рука: 4 сустава-объекта. online = есть ли настоящий робот."""

    def __init__(self, board):
        self.board = board
        self.online = board is not None
        self.joints = [
            Servo(board, SERVO_PINS[i], LIMITS[i][0], LIMITS[i][1], NAMES[i])
            for i in range(4)
        ]
        self.base, self.shoulder, self.elbow, self.grip = self.joints
        for i in range(4):                # выставить стартовые углы
            self.set(i, START[i])

    def set(self, joint, angle):
        """Поставить сустав joint (0..3) на угол."""
        self.joints[joint].angle = angle

    def angles(self):
        """Текущие углы всех суставов списком [a0, a1, a2, a3]."""
        return [s.angle for s in self.joints]

    def close(self):
        if self.board is not None:
            self.board.shutdown()


def connect():
    """Подключиться к роботу. Нет робота — вернётся «режим показа»."""
    try:
        from pymata4 import pymata4
    except ImportError:
        print("⚠ Нет pymata4 (pip install pymata4). Режим показа — без робота.")
        return Arm(None)
    try:
        board = pymata4.Pymata4()         # сам найдёт Arduino по USB
        print("✅ Робот подключён (Firmata).")
        return Arm(board)
    except Exception as e:
        print("⚠ Робот не подключён — режим показа:", e)
        return Arm(None)
