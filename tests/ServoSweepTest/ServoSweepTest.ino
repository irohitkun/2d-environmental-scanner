#include <Servo.h>

Servo tracker;

void setup() {
  tracker.attach(9);
}

void loop() {
  tracker.write(0);
  delay(1000);

  tracker.write(90);
  delay(1000);

  tracker.write(180);
  delay(1000);
}