/*
  one_servo_test.ino — проверяем ОДИН сервопривод и центрируем его в 90°
  через драйвер PCA9685. Удобно при сборке: воткнул серво в КАНАЛ 0, залил —
  он встал в центр. Хочешь увидеть движение? Раскомментируй блок в loop().

  Подключение (минимум, см. урок 6):
    Nano A4 -> SDA, A5 -> SCL, 5V -> VCC и V+, GND -> GND
    проверяемый серво -> КАНАЛ 0 платы PCA9685
  Нужна библиотека "Adafruit PWM Servo Driver Library".
*/
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();   // 0x40
const int CHANNEL = 0;
const int SERVOMIN = 150;
const int SERVOMAX = 600;

int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {
  pwm.begin();
  pwm.setPWMFreq(50);
  pwm.setPWM(CHANNEL, 0, angleToPulse(90));   // центр — нужно перед сборкой
}

void loop() {
  // --- качание (проверка, что серво живой) ---
  // pwm.setPWM(CHANNEL, 0, angleToPulse(60));  delay(500);
  // pwm.setPWM(CHANNEL, 0, angleToPulse(120)); delay(500);
}
