/*
  serial_servos.ino — ОСНОВНАЯ прошивка робота.
  Слушает USB-порт и крутит сервоприводы по командам с компьютера (из pygame).

  Формат команды (одна строка): "номер,угол\n"
    номер: 0=база, 1=плечо, 2=локоть, 3=захват
    угол:  0..180 (лишнее само обрежется лимитами ниже)
  Примеры:  "0,90"   "3,20"   "1,120"

  Подключение сигнальных проводов:
    база -> 3,  плечо -> 5,  локоть -> 6,  захват -> 9
  Питание сервоприводов — ВНЕШНИЕ 5–6 В, общая земля с Arduino.

  Скорость порта 9600 — такая же должна быть в коде на Python (pyserial).
*/
#include <Servo.h>

const int PINS[4] = {3, 5, 6, 9};
// Безопасные пределы углов для каждого сустава (подбери под свою сборку!)
const int LO[4] = {0, 30, 30, 20};
const int HI[4] = {180, 150, 150, 120};

Servo servos[4];
String buf = "";

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 4; i++) {
    servos[i].attach(PINS[i]);
    servos[i].write(90);          // старт — все в центре
  }
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {              // строка дочитана — разбираем
      int comma = buf.indexOf(',');
      if (comma > 0) {
        int i = buf.substring(0, comma).toInt();
        int angle = buf.substring(comma + 1).toInt();
        if (i >= 0 && i < 4) {
          if (angle < LO[i]) angle = LO[i];   // не пускаем за пределы
          if (angle > HI[i]) angle = HI[i];
          servos[i].write(angle);
        }
      }
      buf = "";                   // готовимся к следующей строке
    } else if (c != '\r') {
      buf += c;                   // копим символы строки
    }
  }
}
