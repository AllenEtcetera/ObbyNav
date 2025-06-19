import serial
import time
import RPi.GPIO as GPIO

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
minDist = 10
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_command(cmd):
    ser.write(cmd.encode())
    print(f"Sent: {cmd}")

def read_distance(source='front'):
    command = 'E' if source == 'front' else 'e'
    ser.flushInput()
    ser.write(command.encode())
    time.sleep(0.05)  # short pause to let Arduino respond
    try:
        line = ser.readline().decode('utf-8').strip()
        return float(line)
    except (ValueError, UnicodeDecodeError):
        return 1000  # return a large default distance on failure

def decision_loop():
    while True:
        front_distance = read_distance('front')
        print(f"Front distance: {front_distance} cm")
        if front_distance < minDist:
            send_command('s')
            #send_command('BEEP')  # Optional — if Arduino handles it
            time.sleep(0.5)
            send_command('l')
            time.sleep(0.5)
            send_command('f')
        else:
            send_command('f')
        time.sleep(0.1)

try:
    decision_loop()
except KeyboardInterrupt:
    send_command('s')
    GPIO.cleanup()
    ser.close()
