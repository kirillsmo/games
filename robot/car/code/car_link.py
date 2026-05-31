"""
car_link.py — связь с робомашинкой по Bluetooth.

Bluetooth — это тот же serial-порт, только «по воздуху». Открываем порт машины
и шлём ей короткие команды строкой: "F,200" (вперёд на скорости 200), "S" (стоп).
А машина шлёт нам назад телеметрию: "D,угол,см" (что видит ультразвук) и
"T,л,с,п" (датчики линии: слева/середина/справа).

Если машина не подключена (или нет pyserial) — работает «режим показа»:
ничего не ломается, команды игнорируются, а телеметрия выдаётся понарошку,
чтобы радар крутился даже без машины. Так можно писать код заранее.

Использование:
    from car_link import connect
    car = connect()            # сам найдёт машину
    car.send("F,200")          # вперёд на скорости 200 (0..255)
    car.send("S")              # стоп
    line = car.read()          # строка телеметрии или None
    car.close()
"""
import glob

BAUD = 9600                    # должно совпадать со скоростью в Arduino


def find_port():
    """Ищем машину. Сначала Bluetooth (rfcomm), потом провод (USB)."""
    ports = (
        glob.glob("/dev/rfcomm*")      # Bluetooth-модуль — главный способ
        + glob.glob("/dev/ttyUSB*")    # модуль/адаптер по проводу
        + glob.glob("/dev/ttyACM*")    # сама плата Arduino по USB-кабелю
    )
    return ports[0] if ports else None


class Car:
    """Настоящая машина через serial-порт (Bluetooth или USB)."""

    online = True

    def __init__(self, port=None, baud=BAUD):
        import serial                   # импортируем тут — чтобы без него тоже работало
        port = port or find_port()
        if port is None:
            raise RuntimeError("Не нашёл машину — проверь Bluetooth/кабель.")
        self.ser = serial.Serial(port, baud, timeout=1)
        print("✅ Машина подключена:", port)

    def send(self, cmd):
        """Отправить команду строкой, напр. 'F,200' или 'S'."""
        self.ser.write((cmd + "\n").encode())

    def read(self):
        """Вернуть строку телеметрии ('D,90,40') или None, если данных нет."""
        if self.ser.in_waiting:
            line = self.ser.readline().decode(errors="ignore").strip()
            return line or None
        return None

    def close(self):
        self.ser.close()


class _Offline:
    """Заглушка, когда машины нет: команды игнорируются, телеметрия — понарошку."""

    online = False

    def __init__(self):
        self.angle = 0             # «серво» качается 0..180 и обратно
        self.step = 6
        self.tick = 0

    def send(self, cmd):
        pass

    def read(self):
        self.tick += 1
        if self.tick % 9 == 0:
            return "T,0,1,0"               # понарошку: линию видит середина
        # двигаем «серво» туда-сюда
        self.angle += self.step
        if self.angle >= 180 or self.angle <= 0:
            self.step = -self.step
            self.angle = max(0, min(180, self.angle))
        # понарошку: прямо по курсу (около 90°) — близкая «стена»
        near = 1.0 - abs(self.angle - 90) / 90.0      # 1 в центре, 0 по краям
        cm = int(85 - 70 * near)                      # ~15 см в центре, ~85 по краям
        return "D," + str(self.angle) + "," + str(cm)

    def close(self):
        pass


def connect(port=None):
    """Подключиться к машине. Нет машины — вернётся «режим показа»."""
    try:
        import serial  # noqa: F401
    except ImportError:
        print("⚠ Нет pyserial (pip install pyserial). Режим показа — без машины.")
        return _Offline()
    try:
        return Car(port)
    except Exception as e:
        print("⚠ Машина не подключена — режим показа:", e)
        return _Offline()
