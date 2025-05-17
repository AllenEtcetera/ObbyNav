import serial
import time
import RPi.GPIO as GPIO

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_command(cmd):
    ser.write(cmd.encode())
    print(f"Sent: {cmd}")

def read_distance(sensor_pin):
    # use GPIO pins to read ultrasonic data
    pass

def decision_loop():
    while True:
        front_distance = read_distance('front')
        if front_distance < 20:
            send_command('S')
            send_command('BEEP')
            time.sleep(0.5)
            send_command('L')
            time.sleep(1)
            send_command('F')
        else:
            send_command('F')
        time.sleep(0.1)

try:
    decision_loop()
except KeyboardInterrupt:
    send_command('S')
    GPIO.cleanup()
