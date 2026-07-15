#include <Servo.h>

// Pin configuration
const int SERVO_PIN = 9;
const int TRIG_PIN = 10;
const int ECHO_PIN = 11;

// Scanner configuration
const int MIN_ANGLE = 15;
const int MAX_ANGLE = 165;
const int ANGLE_STEP = 2;

Servo scannerServo;


// Measures distance using the HC-SR04
float measureDistance() {

  // Ensure trigger starts LOW
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Send 10 microsecond trigger pulse
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure echo duration
  long duration = pulseIn(ECHO_PIN, HIGH);

  // Convert time to distance in centimeters
  float distance = duration * 0.0343 / 2.0;

  return distance;
}


void setup() {

  Serial.begin(9600);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  scannerServo.attach(SERVO_PIN);

  // Start at minimum scanning angle
  scannerServo.write(MIN_ANGLE);

  delay(500);
}


void loop() {

  // Scan from left to right
  for (int angle = MIN_ANGLE; angle <= MAX_ANGLE; angle += ANGLE_STEP) {

    scannerServo.write(angle);

    // Give servo time to reach position
    delay(30);

    float distance = measureDistance();

    // Output format: angle,distance
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }


  // Scan from right to left
  for (int angle = MAX_ANGLE; angle >= MIN_ANGLE; angle -= ANGLE_STEP) {

    scannerServo.write(angle);

    delay(30);

    float distance = measureDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}