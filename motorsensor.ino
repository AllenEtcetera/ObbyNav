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

Servo headServo;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_FRONT, OUTPUT);
  pinMode(ECHO_FRONT, INPUT);
  pinMode(TRIG_BACK, OUTPUT);
  pinMode(ECHO_BACK, INPUT);
  pinMode(BUZZER, OUTPUT);
  headServo.attach(8);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    executeCommand(cmd);
  }
}

void executeCommand(char cmd) {
  switch (cmd) {
    case 'F': moveForward(); break;
    case 'B': moveBackward(); break;
    case 'L': turnLeft(); break;
    case 'R': turnRight(); break;
    case 'S': stopMotors(); break;
    case 'BEEP': beep(); break;
  }
}

// motor and beep logic functions here...
