/*
  serial_servos.ino — ОСНОВНАЯ прошивка робота (драйвер PCA9685).
  Слушает USB-порт и крутит сервоприводы по командам с компьютера (из pygame).

  Формат команды (одна строка): "номер,угол\n"
    номер: 0=база, 1=плечо, 2=локоть, 3=захват  (это КАНАЛЫ PCA9685)
    угол:  0..180 (лишнее само обрежется лимитами ниже)
  Примеры:  "0,90"   "3,20"   "1,120"

  Подключение (см. урок 6):
    Nano A4 -> PCA9685 SDA,  Nano A5 -> PCA9685 SCL
    Nano 5V -> PCA9685 VCC,  Nano GND -> PCA9685 GND
    Nano 5V -> PCA9685 V+    (питание серво идёт от USB через 5V Nano)
    серво -> каналы 0,1,2,3 платы PCA9685
  Нужна библиотека: "Adafruit PWM Servo Driver Library" (поставить в Arduino IDE).

  Скорость порта 9600 — такая же должна быть в коде на Python (pyserial).
*/
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();   // адрес по умолчанию 0x40

// Безопасные пределы углов для каждого сустава (подбери под свою сборку!)
const int LO[4] = {0, 30, 30, 20};
const int HI[4] = {180, 150, 150, 120};

// Длина импульса для PCA9685 (из 4096) при 50 Гц: ~150 = 0°, ~600 = 180°
const int SERVOMIN = 150;
const int SERVOMAX = 600;

String buf = "";

int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(50);                 // сервоприводы работают на 50 Гц
  for (int i = 0; i < 4; i++) {
    pwm.setPWM(i, 0, angleToPulse(90));   // старт — все в центре
  }
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {                  // строка дочитана — разбираем
      int comma = buf.indexOf(',');
      if (comma > 0) {
        int i = buf.substring(0, comma).toInt();
        int angle = buf.substring(comma + 1).toInt();
        if (i >= 0 && i < 4) {
          if (angle < LO[i]) angle = LO[i];   // не пускаем за пределы
          if (angle > HI[i]) angle = HI[i];
          pwm.setPWM(i, 0, angleToPulse(angle));
        }
      }
      buf = "";                       // готовимся к следующей строке
    } else if (c != '\r') {
      buf += c;                       // копим символы строки
    }
  }
}
