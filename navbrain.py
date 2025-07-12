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

def scan_head():
    ser.flushInput()
    send_command('h')
    time.sleep(0.3)
    try:
        line = ser.readline().decode('utf-8').strip()
        print(f"Scanned:{line}")
        parts = line.split(',')
        scanData = {}
        for i in parts:
            lbl, dist = i.split(':')
            scanData[lbl] = float(dist)
        return scanData
    except Exception as e:
        print(f"Scan failed: {e}")
        return {'L': 1000, 'C': 1000, 'R': 1000}

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
        frontDist = read_distance('front')
        backDist = read_distance('back')
        print(f"Front distance: {frontDist} cm")
        print(f"Back distance: {backDist} cm")
        if frontDist < minDist:
            send_command('s')
            time.sleep(0.25)
            scanData = scan_head()
            print(scanData)
            bestDir = max(scanData, key=scanData.get)
            maxDist = scanData[bestDir]
            if maxDist > minDist:
                if bestDir == 'L': # If left has more distance, go left
                    send_command('l')
                    time.sleep(0.25)
                elif bestDir == 'R': # If right has more distance, go right
                    send_command('r')
                    time.sleep(0.25)
                send_command('f') # No turn if already centered
            else:
                if backDist < minDist:
                    send_command('s')
                    send_command('A')
                    time.sleep(0.25)
                    send_command('A')
                else:
                    send_command('b')
                    time.sleep(0.25)
                    send_command('s')
        else:
            send_command('f')
        
try:
    decision_loop()
except KeyboardInterrupt:
    send_command('s')
    GPIO.cleanup()
    ser.close()
