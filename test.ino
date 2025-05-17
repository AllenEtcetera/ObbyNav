#include <Servo.h>

#define TRIG_FRONT 7
#define ECHO_FRONT 6
#define TRIG_BACK 5
#define ECHO_BACK 4
#define LEFT_MOTOR_FWD 9
#define LEFT_MOTOR_BWD 10
#define RIGHT_MOTOR_FWD 11
#define RIGHT_MOTOR_BWD 12
#define BUZZER 3
#define SERVO_PIN 8

Servo headServo;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_FRONT, OUTPUT);
  pinMode(ECHO_FRONT, INPUT);
  pinMode(TRIG_BACK, OUTPUT);
  pinMode(ECHO_BACK, INPUT);
  pinMode(LEFT_MOTOR_FWD, OUTPUT);
  pinMode(LEFT_MOTOR_BWD, OUTPUT);
  pinMode(RIGHT_MOTOR_FWD, OUTPUT);
  pinMode(RIGHT_MOTOR_BWD, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  headServo.attach(SERVO_PIN);

  Serial.println("ObbyNav Hardware Test Starting...");
}

void loop() {
  testMotors();
  testSensors();
  testServo();
  testBuzzer();
  delay(5000);  // Wait before restarting tests
}

void testMotors() {
  Serial.println("Testing motors...");
  digitalWrite(LEFT_MOTOR_FWD, HIGH);
  digitalWrite(RIGHT_MOTOR_FWD, HIGH);
  delay(1000);
  digitalWrite(LEFT_MOTOR_FWD, LOW);
  digitalWrite(RIGHT_MOTOR_FWD, LOW);

  digitalWrite(LEFT_MOTOR_BWD, HIGH);
  digitalWrite(RIGHT_MOTOR_BWD, HIGH);
  delay(1000);
  digitalWrite(LEFT_MOTOR_BWD, LOW);
  digitalWrite(RIGHT_MOTOR_BWD, LOW);
}

long readDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000);  // timeout 30ms
  long distance = duration * 0.034 / 2;
  return distance;
}

void testSensors() {
  Serial.print("Front Sensor: ");
  Serial.print(readDistance(TRIG_FRONT, ECHO_FRONT));
  Serial.println(" cm");

  Serial.print("Back Sensor: ");
  Serial.print(readDistance(TRIG_BACK, ECHO_BACK));
  Serial.println(" cm");
}

void testServo() {
  Serial.println("Testing servo...");
  headServo.write(0);
  delay(500);
  headServo.write(90);
  delay(500);
  headServo.write(180);
  delay(500);
  headServo.write(90); // Return to center
}

void testBuzzer() {
  Serial.println("Beeping buzzer...");
  digitalWrite(BUZZER, HIGH);
  delay(200);
  digitalWrite(BUZZER, LOW);
}
