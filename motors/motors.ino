#include <Servo.h>

// Wheels
int IN1 = 7;
int IN2 = 8;
int ENA = 5;

int IN3 = 9;
int IN4 = 10;
int ENB = 6;

int SPEED = 100;

// Front HC-SR04
const int trigFront = 2;
const int echoFront = 3;

// Back HC-SR04
const int trigBack = 12;
const int echoBack = 13;

// SG90 Servo Motor
Servo head;
const int servoPin = 11;

char input;

void setup(){
  // Wheels
  pinMode(IN1, OUTPUT);// A
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT);// B
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  analogWrite(ENA, 255);  // Full speed
  analogWrite(ENB, 255);

  // Ultrasonics
  pinMode(trigFront, OUTPUT); // Front (E)
  pinMode(echoFront, INPUT);
  pinMode(trigBack, OUTPUT); // Back (e)
  pinMode(echoBack, INPUT);

  // Start serial communication
  Serial.begin(9600);
  head.attach(servoPin);
  head.write(90);  // Center position

  
}
void forward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}
void backward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}
void turnLeft() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}
void turnRight() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}
void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
void scanHead() {
  long leftDist, centerDist, rightDist;

  Servo.write(0);    // Left
  delay(500);
  leftDist = measureDistance();

  Servo.write(90);   // Center
  delay(500);
  centerDist = measureDistance();

  Servo.write(180);  // Right
  delay(500);
  rightDist = measureDistance();

  Serial.print("L:");
  Serial.print(leftDist);
  Serial.print(",C:");
  Serial.print(centerDist);
  Serial.print(",R:");
  Serial.println(rightDist);
}
long getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.034 / 2;
  return distance;
}
void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    switch (cmd) {
      case 'h':
        scanHead();
        break;
      case 'f':  // forward
        forward();
        break;
      case 'b':  // backward
        backward();
        break;
      case 'l':  // turn left
        turnLeft();
        break;
      case 'r':  // turn right
        turnRight();
        break;
      case 's':  // stop
        stopMotors();
        break;
      case 'E': Serial.println(getDistance(trigFront, echoFront)); break;
      case 'e': Serial.println(getDistance(trigBack, echoBack)); break;
    }
  }
 } 
