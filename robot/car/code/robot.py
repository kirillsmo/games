"""
robot.py — управление робомашинкой из Python через Firmata.

Никакого своего протокола! Один раз заливаем в Arduino стандартную прошивку
FirmataExpress (см. arduino/README.txt). Дальше плата слушается компьютера, а весь
«ум» машины живёт в Python. Библиотека pymata4 сама управляет ножками, а мы прячем
её за понятными объектами: car.left / car.right (моторы), car.radar, car.line.

Использование:
    from robot import connect
    car = connect()
    car.forward(180)       # вперёд на скорости 180 (0..255)
    car.left_turn()        # поворот налево «танком»
    car.stop()
    cm = car.radar.measure()       # померить расстояние спереди
    l, m, r = car.line.read()      # датчики линии (0/1)
    car.close()

Нет машины (или нет pymata4) — «режим показа»: код не падает, моторы молчат,
а радар и линия выдают данные понарошку, чтобы можно было писать код заранее.

Установка библиотеки:  pip install pymata4

ПОДКЛЮЧЕНИЕ (сверь с реальной платой — пины могут отличаться!):
    L298N левые:  ENA=5, IN1=7, IN2=8     правые: ENB=6, IN3=9, IN4=11
    Серво радара: D3      Ультразвук HC-SR04: TRIG=12, ECHO=13
    Датчики линии: A0/A1/A2  (на Uno это ножки 14/15/16)
"""
import math


class Motor:
    """Один борт моторов через H-мост L298N. drive(speed): -255..255."""

    def __init__(self, board, en, in1, in2):
        self.board, self.en, self.in1, self.in2 = board, en, in1, in2
        self.trim = 1.0            # калибровка: 0.9 = чуть медленнее (см. урок 8)
        if board is not None:
            board.set_pin_mode_pwm_output(en)
            board.set_pin_mode_digital_output(in1)
            board.set_pin_mode_digital_output(in2)

    def drive(self, speed):
        """+ вперёд, − назад, 0 стоп. Учитывает калибровку trim."""
        speed = int(max(-255, min(255, speed)) * self.trim)
        if self.board is None:
            return
        self.board.digital_write(self.in1, 1 if speed > 0 else 0)
        self.board.digital_write(self.in2, 1 if speed < 0 else 0)
        self.board.pwm_write(self.en, abs(speed))

    def stop(self):
        self.drive(0)


class Radar:
    """Серво качает ультразвук. look(angle) — повернуть, measure() — см до стены."""

    def __init__(self, board, servo, trig, echo):
        self.board, self.servo, self.trig = board, servo, trig
        self.angle = 90
        self.distance = 200
        self._sim_dir = 6          # для режима показа
        if board is not None:
            board.set_pin_mode_servo(servo)
            board.set_pin_mode_sonar(trig, echo)

    def look(self, angle):
        self.angle = int(max(0, min(180, angle)))
        if self.board is not None:
            self.board.servo_write(self.servo, self.angle)

    def measure(self):
        """Вернуть расстояние спереди в см (и запомнить в self.distance)."""
        if self.board is not None:
            cm = self.board.sonar_read(self.trig)[0]
            self.distance = cm if cm else 200
        else:                                      # режим показа — «стена» по центру
            near = 1.0 - abs(self.angle - 90) / 90.0
            self.distance = int(85 - 70 * max(0, near))
        return self.distance


class LineSensor:
    """3 датчика линии слева/центр/справа. read() -> [0/1, 0/1, 0/1]."""

    def __init__(self, board, pins):
        self.board, self.pins = board, pins
        self._tick = 0
        if board is not None:
            for p in pins:
                board.set_pin_mode_digital_input(p)

    def read(self):
        if self.board is not None:
            return [self.board.digital_read(p)[0] for p in self.pins]
        self._tick += 1                            # режим показа
        return [0, 1, 0] if self._tick % 30 < 5 else [0, 0, 0]


class Car:
    """Вся машина: два борта моторов + радар + датчики линии."""

    def __init__(self, board):
        self.board = board
        self.online = board is not None
        self.left = Motor(board, 5, 7, 8)
        self.right = Motor(board, 6, 9, 11)
        self.radar = Radar(board, servo=3, trig=12, echo=13)
        self.line = LineSensor(board, [14, 15, 16])

    def forward(self, speed=180):
        self.left.drive(speed);  self.right.drive(speed)

    def back(self, speed=180):
        self.left.drive(-speed); self.right.drive(-speed)

    def left_turn(self, speed=180):                # поворот «танком»
        self.left.drive(-speed); self.right.drive(speed)

    def right_turn(self, speed=180):
        self.left.drive(speed);  self.right.drive(-speed)

    def stop(self):
        self.left.stop(); self.right.stop()

    def close(self):
        self.stop()
        if self.board is not None:
            self.board.shutdown()


def connect():
    """Подключиться к машине. Нет машины — вернётся «режим показа»."""
    try:
        from pymata4 import pymata4
    except ImportError:
        print("⚠ Нет pymata4 (pip install pymata4). Режим показа — без машины.")
        return Car(None)
    try:
        board = pymata4.Pymata4()      # по USB; для Bluetooth: Pymata4(com_port="/dev/rfcomm0")
        print("✅ Машина подключена (Firmata).")
        return Car(board)
    except Exception as e:
        print("⚠ Машина не подключена — режим показа:", e)
        return Car(None)
