/*
  drive_test.ino — ПЕРВАЯ ЖИЗНЬ машины (урок 3).
  Проверяем, что моторы и драйвер L298N работают: машина едет вперёд 2 секунды,
  потом останавливается навсегда.

  ВАЖНО: подними машину на подставку (коробок), чтобы колёса крутились в воздухе,
  а не уехала со стола!

  Подключение к драйверу L298N (сверь с реальной платой — пины могут отличаться):
    левые моторы:  ENA(скорость)=5,  IN1=7,  IN2=8
    правые моторы: ENB(скорость)=6,  IN3=9,  IN4=11
  Скорость 0..255 задаём через analogWrite на ENA/ENB.
*/
const int ENA = 5, IN1 = 7, IN2 = 8;     // левые моторы
const int ENB = 6, IN3 = 9, IN4 = 11;    // правые моторы

void setup() {
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);

  // едем вперёд: оба мотора крутятся «вперёд»
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, 200);                  // скорость левых
  analogWrite(ENB, 200);                  // скорость правых
  delay(2000);                            // 2 секунды

  // стоп
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void loop() {
  // ничего — машина уже остановилась
}
