// Wheels
int In1 = 7;
int In2 = 8;
int ENA = 5;

int In3 = 9;
int In4 = 10;
int ENB = 6;

int SPEED = 100;

// Front HC-SR04
const int trigFront = 2;
const int echoFront = 3;

// Back HC-SR04
const int trigBack = 12;
const int echoBack = 13;

// SG90 Servo Motor
const int servoPin = 11;

char input;

void setup(){
  // Wheels
  pinMode(In1, OUTPUT);// A
  pinMode(In2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(In3, OUTPUT);// B
  pinMode(In4, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Ultrasonics
  pinMode(trigFront, OUTPUT); // Front (E)
  pinMode(echoFront, INPUT);
  pinMode(trigBack, OUTPUT); // Back (e)
  pinMode(echoBack, INPUT);

  // Start serial communication
  Serial.begin(9600);
  
}
void forward() {
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
void backward() {
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void turnLeft() {
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
void turnRight() {
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void stopMotors() {
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
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
