/*
  serial_drive.ino — езда по командам (урок 4).
  Машина слушает Serial-порт и едет по командам с компьютера.

  Формат команды (одна строка):
    "F,200"  вперёд на скорости 200 (0..255)
    "B,200"  назад
    "L,200"  поворот налево  (левые моторы назад, правые вперёд — «танком»)
    "R,200"  поворот направо
    "S"      стоп

  Пока что команды шлём из Serial Monitor по USB-кабелю. В уроке 5 тот же
  Serial станет Bluetooth — и провод будет не нужен.

  Драйвер L298N (сверь с реальной платой):
    левые:  ENA=5, IN1=7, IN2=8     правые: ENB=6, IN3=9, IN4=11
  Скорость порта 9600 — такая же в коде на Python.
*/
const int ENA = 5, IN1 = 7, IN2 = 8;
const int ENB = 6, IN3 = 9, IN4 = 11;

String buf = "";

void leftMotors(int dir, int speed) {     // dir: +1 вперёд, -1 назад, 0 стоп
  digitalWrite(IN1, dir > 0 ? HIGH : LOW);
  digitalWrite(IN2, dir < 0 ? HIGH : LOW);
  analogWrite(ENA, dir == 0 ? 0 : speed);
}

void rightMotors(int dir, int speed) {
  digitalWrite(IN3, dir > 0 ? HIGH : LOW);
  digitalWrite(IN4, dir < 0 ? HIGH : LOW);
  analogWrite(ENB, dir == 0 ? 0 : speed);
}

void doCommand(char dir, int speed) {
  if (speed < 0) speed = 0;
  if (speed > 255) speed = 255;
  if (dir == 'F') { leftMotors(1, speed);  rightMotors(1, speed); }
  else if (dir == 'B') { leftMotors(-1, speed); rightMotors(-1, speed); }
  else if (dir == 'L') { leftMotors(-1, speed); rightMotors(1, speed); }
  else if (dir == 'R') { leftMotors(1, speed);  rightMotors(-1, speed); }
  else { leftMotors(0, 0); rightMotors(0, 0); }   // 'S' и всё прочее — стоп
}

void setup() {
  Serial.begin(9600);
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  doCommand('S', 0);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      char dir = buf.length() > 0 ? buf.charAt(0) : 'S';
      int comma = buf.indexOf(',');
      int speed = comma > 0 ? buf.substring(comma + 1).toInt() : 200;
      doCommand(dir, speed);
      buf = "";
    } else if (c != '\r') {
      buf += c;
    }
  }
}
