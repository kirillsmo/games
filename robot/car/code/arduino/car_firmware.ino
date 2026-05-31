/*
  car_firmware.ino — ОСНОВНАЯ прошивка робомашинки (уроки 5–6, 7–11).
  Машина слушает команды (по Bluetooth или USB) и шлёт назад телеметрию.

  КОМАНДЫ от компьютера (одна строка):
    "F,200" вперёд · "B,200" назад · "L,200" налево · "R,200" направо · "S" стоп
    "SCAN,1" включить качание датчика и слать расстояние · "SCAN,0" выключить

  ТЕЛЕМЕТРИЯ машине → компьютеру:
    "D,угол,см"   — ультразвук под углом серво (угол 0..180, см)
    "T,л,с,п"     — датчики линии: слева/середина/справа (1 = видит линию)

  ПОДКЛЮЧЕНИЕ (сверь с реальной платой — пины могут отличаться!):
    Драйвер L298N: левые ENA=5,IN1=7,IN2=8 · правые ENB=6,IN3=9,IN4=11
    Серво (качает датчик):  пин 3
    Ультразвук HC-SR04:     TRIG=12, ECHO=13
    Датчики линии:          A0 (слева), A1 (середина), A2 (справа)
    Bluetooth-модуль:       TX→RX(0), RX→TX(1) платы (это и есть Serial)

  Скорость порта 9600 — такая же в Bluetooth-модуле и в коде на Python.
  Нужна стандартная библиотека Servo (уже есть в Arduino IDE).
*/
#include <Servo.h>

const int ENA = 5, IN1 = 7, IN2 = 8;
const int ENB = 6, IN3 = 9, IN4 = 11;
const int SERVO_PIN = 3;
const int TRIG = 12, ECHO = 13;
const int LINE_L = A0, LINE_M = A1, LINE_R = A2;

Servo radar;
String buf = "";

bool scanning = false;
int angle = 90;                 // текущий угол серво
int dir = 6;                    // шаг качания (туда-сюда)

unsigned long lastLine = 0;     // когда последний раз слали датчики линии

void leftMotors(int d, int s) {
  digitalWrite(IN1, d > 0 ? HIGH : LOW);
  digitalWrite(IN2, d < 0 ? HIGH : LOW);
  analogWrite(ENA, d == 0 ? 0 : s);
}
void rightMotors(int d, int s) {
  digitalWrite(IN3, d > 0 ? HIGH : LOW);
  digitalWrite(IN4, d < 0 ? HIGH : LOW);
  analogWrite(ENB, d == 0 ? 0 : s);
}

void doCommand(char c, int s) {
  if (s < 0) s = 0;
  if (s > 255) s = 255;
  if (c == 'F') { leftMotors(1, s);  rightMotors(1, s); }
  else if (c == 'B') { leftMotors(-1, s); rightMotors(-1, s); }
  else if (c == 'L') { leftMotors(-1, s); rightMotors(1, s); }
  else if (c == 'R') { leftMotors(1, s);  rightMotors(-1, s); }
  else { leftMotors(0, 0); rightMotors(0, 0); }
}

long readDistance() {           // расстояние ультразвуком, в см
  digitalWrite(TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long us = pulseIn(ECHO, HIGH, 25000);   // ждём эхо, но не дольше ~4 м
  if (us == 0) return 200;                // ничего не услышали — «далеко»
  return us / 58;                         // микросекунды → сантиметры
}

void handleLine(String s) {     // разобрать строку команды
  char c = s.length() > 0 ? s.charAt(0) : 'S';
  int comma = s.indexOf(',');
  if (s.startsWith("SCAN")) {
    scanning = (comma > 0 && s.substring(comma + 1).toInt() == 1);
    if (!scanning) { angle = 90; radar.write(angle); }
    return;
  }
  int speed = comma > 0 ? s.substring(comma + 1).toInt() : 200;
  doCommand(c, speed);
}

void setup() {
  Serial.begin(9600);
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  pinMode(LINE_L, INPUT); pinMode(LINE_M, INPUT); pinMode(LINE_R, INPUT);
  radar.attach(SERVO_PIN);
  radar.write(angle);
  doCommand('S', 0);
}

void loop() {
  // 1) читаем команды
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { handleLine(buf); buf = ""; }
    else if (c != '\r') buf += c;
  }

  // 2) радар: качаем серво и шлём расстояние
  if (scanning) {
    radar.write(angle);
    delay(40);                            // даём серво доехать
    long cm = readDistance();
    Serial.print("D,"); Serial.print(angle); Serial.print(","); Serial.println(cm);
    angle += dir;
    if (angle >= 174 || angle <= 6) dir = -dir;   // развернуть качание
  }

  // 3) датчики линии — раз в ~150 мс
  if (millis() - lastLine > 150) {
    lastLine = millis();
    int l = digitalRead(LINE_L), m = digitalRead(LINE_M), r = digitalRead(LINE_R);
    Serial.print("T,"); Serial.print(l); Serial.print(",");
    Serial.print(m); Serial.print(","); Serial.println(r);
  }
}
