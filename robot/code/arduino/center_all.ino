/*
  center_all.ino — ставит ВСЕ 4 сервопривода в 90° (центр) через PCA9685.
  Заливай ПЕРЕД сборкой и перед креплением качалок, чтобы у суставов был
  полный диапазон в обе стороны.

  Подключение (см. урок 6):
    Nano A4 -> SDA, A5 -> SCL, 5V -> VCC и V+, GND -> GND
    серво -> каналы 0 (база), 1 (плечо), 2 (локоть), 3 (захват)
  Нужна библиотека "Adafruit PWM Servo Driver Library".
*/
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();   // 0x40
const int SERVOMIN = 150;
const int SERVOMAX = 600;

int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {
  pwm.begin();
  pwm.setPWMFreq(50);
  for (int i = 0; i < 4; i++) {
    pwm.setPWM(i, 0, angleToPulse(90));   // центр
  }
}

void loop() {
  // ничего — сервоприводы держат 90°
}
