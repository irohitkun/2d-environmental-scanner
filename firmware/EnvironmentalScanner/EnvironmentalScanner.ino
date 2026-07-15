#include <Servo.h>

// Pin configuration
const int SERVO_PIN = 9;
const int TRIG_PIN = 10;
const int ECHO_PIN = 11;

// Scanner configuration
const int MIN_ANGLE = 15;
const int MAX_ANGLE = 165;
const int ANGLE_STEP = 2;

// Number of ultrasonic readings taken at each angle
const int SAMPLE_COUNT = 3;

Servo scannerServo;


// Take one ultrasonic distance measurement
float measureDistance() {

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  // Timeout after 30 milliseconds if no echo returns
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);

  // No echo received
  if (duration == 0) {
    return -1;
  }

  float distance = duration * 0.0343 / 2.0;

  return distance;
}


// Take multiple measurements and average valid ones
float measureFilteredDistance() {

  float total = 0;
  int validSamples = 0;

  for (int i = 0; i < SAMPLE_COUNT; i++) {

    float distance = measureDistance();

    // Accept only useful sensor readings
    if (distance > 2 && distance < 200) {

      total += distance;
      validSamples++;

    }

    delay(5);
  }

  // No valid measurements
  if (validSamples == 0) {
    return -1;
  }

  return total / validSamples;
}


void setup() {

  Serial.begin(9600);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  scannerServo.attach(SERVO_PIN);

  scannerServo.write(MIN_ANGLE);

  delay(500);
}


void loop() {

  // Left-to-right scan
  for (int angle = MIN_ANGLE;
       angle <= MAX_ANGLE;
       angle += ANGLE_STEP) {

    scannerServo.write(angle);

    delay(30);

    float distance = measureFilteredDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }


  // Right-to-left scan
  for (int angle = MAX_ANGLE;
       angle >= MIN_ANGLE;
       angle -= ANGLE_STEP) {

    scannerServo.write(angle);

    delay(30);

    float distance = measureFilteredDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}
