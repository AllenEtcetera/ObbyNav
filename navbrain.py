#!/usr/bin/env python3
import glob
import serial
import time
import RPi.GPIO as GPIO


# def find_arduino(baud=9600, timeout=1):
#     possible_ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
#     for port in possible_ports:
#         try:
#             ser = serial.Serial(port, baudrate=baud, timeout=timeout)
#             ser.write(b'E')  # 'E' is for front sensor
#             response = ser.readline().decode('utf-8').strip()
#             if response:  # we expect a number like "25.4"
#                 print(f"Arduino detected on {port}")
#                 return ser
#         except (serial.SerialException, UnicodeDecodeError):
#             continue
#     raise IOError("Arduino not found on any serial port.")

# ser = find_arduino()
SERIAL_PORT = '/dev/ttyACM0'
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
            time.sleep(0.25)
            send_command('L:')
            time.sleep(0.25)
            send_command('C:')
            time.sleep(0.25)
            send_command('R:')
            time.sleep(0.25)
            send_command('C:')
            send_command('l')
            send_command('l')
            send_command('l')
            time.sleep(0.25)
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
