#!/usr/bin/env python3
import glob
import serial
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
from pathlib import Path
import datetime


SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
minDist = 40
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
            if ':' not in i:
                continue  # skip bad data
            lbl, dist = i.split(':')
            scanData[lbl] = float(dist)
        return scanData
    except Exception as e:
        print(f"Scan failed: {e}")
        return {'L': 40, 'C': 40, 'R': 40}

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

def cap_door():
    cap = cv2.VideoCapture("/dev/video0")
    filename = datetime.datetime.now().strftime("door_%Y%m%d_%H%M%S.jpg")
    ret, frame = cap.read()
    cap.release()
    if ret:
        cv2.imwrite("live.jpg", frame)
        return find_door("live.jpg", filename)
    if not ret:
        print("Camera capture failed.")

def find_door(path, outPath):
    # Load the image
    imgPath = cv2.imread(str(path))
    image = cv2.resize(imgPath, (640, 480))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    # Hough Transform for lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=100, maxLineGap=10)
    vertical_lines = []
    # Filter vertical lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            if dx < 10 and dy > 50:
                vertical_lines.append((x1, y1, x2, y2))
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 255), 1)  # Yellow = all vertical lines
    # Try to find pairs of vertical lines
    pairs_found = []
    for i in range(len(vertical_lines)):
        for j in range(i + 1, len(vertical_lines)):
            x1a, y1a, x2a, y2a = vertical_lines[i]
            x1b, y1b, x2b, y2b = vertical_lines[j]
            dist = abs(x1a - x1b)
            if 50 < dist < 200:
                mid_x = (x1a + x1b) // 2
                pairs_found.append({
                    "coords": (x1a, x1b),
                    "dist": dist,
                    "center": mid_x,
                    "lines": [(x1a, y1a, x2a, y2a), (x1b, y1b, x2b, y2b)]
                })
                cv2.rectangle(image, (min(x1a, x1b), 0), (max(x1a, x1b), 480), (255, 0, 0), 1)  # Blue = candidate pairs
    # Highlight best (most centered) pair
    cv2.line(image, (320, 0), (320, 480), (200, 200, 200), 1)  # Gray center line
    if pairs_found:
        best_pair = min(pairs_found, key=lambda p: abs(p["center"] - 320))  # 320 = center of image
        xa, xb = best_pair["coords"]
        cv2.rectangle(image, (min(xa, xb), 0), (max(xa, xb), 480), (0, 255, 0), 3)  # Green = best pair
        # Draw individual lines in green for clarity
        for x1, y1, x2, y2 in best_pair["lines"]:
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(f"DOOR FOUND! Saved to {outPath}")
        #cv2.imwrite(outPath, image)
        return True
    else:
        print(f" NO DOOR!")
        return False

def main():
    def decision_loop():
        while True:
            frontDist = read_distance('front')
            backDist = read_distance('back')
            print(f"Front: {frontDist} cm")
            print(f"Back: {backDist} cm")
            if frontDist < minDist:
                send_command('s')
                time.sleep(0.25)
                 # Door check before backing up
                print("Obstacle detected. Checking for doorway...")
                door_path = cap_door()
                if door_path:  # Add logic to verify if door was actually detected
                    print("Doorway detected! Proceeding forward.")
                    send_command('f')
                    time.sleep(1)
                    continue  # skip further logic this cycle
                send_command('b')
                time.sleep(0.5)
                scanData = scan_head()
                print(scanData)
                bestDir = max(scanData, key=scanData.get)
                maxDist = scanData[bestDir]
                if maxDist > minDist:
                    if bestDir == 'L': # If left has more distance, go left
                        send_command('l')
                        time.sleep(0.5)
                    elif bestDir == 'R': # If right has more distance, go right
                        send_command('r')
                        time.sleep(0.5)
                    send_command('f') # No turn if already centered
                else:
                    if backDist < minDist:
                        send_command('s')
                        print("I'm stuck!")
                        for _ in range(3):  # or just once if continuous buzz
                            send_command('A')
                            time.sleep(0.5)
                    else:
                        send_command('b')
                        time.sleep(0.5)
                        send_command('s')

            else:
                send_command('f')

    try:
        decision_loop()
    except KeyboardInterrupt:
        send_command('s')
        GPIO.cleanup()
        ser.close()

if __name__ == "__main__":
    main()


