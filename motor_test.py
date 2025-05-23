import RPi.GPIO as GPIO
from time import sleep

# Pin setup
IN1, IN2, IN3, IN4 = 17, 18, 27, 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def stop():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def forward():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def backward():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

try:
    print("Forward")
    forward()
    sleep(2)
    print("Backward")
    backward()
    sleep(2)
    print("Stop")
    stop()
finally:
    GPIO.cleanup()
