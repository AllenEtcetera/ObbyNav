#!/usr/bin/env python3
import serial
import time
import cv2
import numpy as np
import os
import datetime

# Establish serial connection to Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Send command to Arduino and print for debug
def send_command(cmd):
    ser.write(cmd.encode())
    ser.flush()
    if cmd != 'f': # Don't print forward command
        print(f"Sent: {cmd}")

# Parse Arduino's head scan serial output into dict
def scan_head():
    ser.flushInput()
    send_command('h')
    time.sleep(3.0)
    try:
        line = ser.readline().decode('utf-8').strip()
        print(f"Scanned:{line}")
        parts = line.split(',')
        scanData = {}
        for i in parts:
            if ':' not in i:
                continue  # skip bad data
            lbl, dist = i.split(':')
            try:
                scanData[lbl] = float(dist)
            except ValueError:
                scanData[lbl] = 0
        for k in ['L','C','R']:
            if k not in scanData:
                scanData[k] = 0
        return scanData
    except Exception as e:
        print(f"Scan failed: {e}")
        return {'L': 0, 'C': 0, 'R': 0}

# Read distance from a specific sensor on Arduino
def read_distance(source='front'):
    command = 'E' if source == 'front' else 'e'
    ser.flushInput()
    ser.write(command.encode())
    time.sleep(0.05)  # short pause to let Arduino respond
    try:
        line = ser.readline().decode('utf-8').strip()
        return float(line)
    except (ValueError, UnicodeDecodeError):
        return 1000  # return large distance on failure

# Capture image and check for doorway presence
def cap_door():
    filename = datetime.datetime.now().strftime("door_%Y%m%d_%H%M%S.jpg")
    fullPath = f"frames/{filename}"
    # Ensure output directory exists
    if not os.path.exists("frames"):
        os.makedirs("frames")
    # Capture using libcamera-jpeg with no preview, and verbose error reporting
    result = os.system(f"libcamera-jpeg -o {fullPath} --width 640 --height 480 --nopreview --timeout 1000")
    if result != 0 or not os.path.exists(fullPath):
        print(f"Camera capture failed or file not created: {fullPath}")
        return False
    return find_door(fullPath, filename)

# Determine if a doorway is present in a given image file
def find_door(path, name):
    # Load the image
    imgPath = cv2.imread(str(path))
    if imgPath is None:
        print("Failed to read image.")
        return False
    # Flip image
    img = cv2.rotate(imgPath, cv2.ROTATE_180)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Edge detection, Hough
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=100, maxLineGap=10)
    vertLines = []
    # Filter vertical lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            if dx < 10 and dy > 50:
                vertLines.append((x1, y1, x2, y2))
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1)  # Yellow = all vertical lines
    # Try to find pairs of vertical lines
    pairs = []
    for i in range(len(vertLines)):
        for j in range(i + 1, len(vertLines)):
            x1a, y1a, x2a, y2a = vertLines[i]
            x1b, y1b, x2b, y2b = vertLines[j]
            dist = abs(x1a - x1b)
            if 50 < dist < 200:
                mid_x = (x1a + x1b) // 2
                pairs.append({
                    "coords": (x1a, x1b),
                    "dist": dist,
                    "center": mid_x,
                    "lines": [(x1a, y1a, x2a, y2a), (x1b, y1b, x2b, y2b)]
                })
                cv2.rectangle(img, (min(x1a, x1b), 0), (max(x1a, x1b), 480), (255, 0, 0), 1)  # Blue = candidate pairs
    cv2.line(img, (320, 0), (320, 480), (200, 200, 200), 1)  # Gray center line
    if pairs:
        bestPair = min(pairs, key=lambda p: abs(p["center"] - 320))  # 320 = center of image
        xa, xb = bestPair["coords"]
        cv2.rectangle(img, (min(xa, xb), 0), (max(xa, xb), 480), (0, 255, 0), 3)  # Green = best pair
        # Draw individual lines in green for clarity
        for x1, y1, x2, y2 in bestPair["lines"]:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(f"DOOR FOUND! Saved to {name}")
        cv2.imwrite(name, img)
        return True
    else:
        print(f"NO DOOR!")
        return False

# Select the most open direction from scan results
def choose_direction(scanData):
    bestDir = max(scanData, key=scanData.get)
    print(f"Scanned:{scanData}\nBest Direction: {bestDir} at {scanData[bestDir]}")
    return bestDir

# Main behavior loop for navigation and decisions
def decision_loop():
    minDist = 20
    while True:
        frontDist = read_distance('front')
        backDist = read_distance('back')
        print(f"Front: {frontDist} cm\nBack: {backDist} cm")
        if frontDist < minDist:
            send_command('s')
            print("Obstacle detected. Checking for doorway...")
            if cap_door(): # Add logic to verify if door detected
                print("Doorway detected! Proceeding forward.")
                send_command('f')
                continue
            else:
                send_command('b')
                time.sleep(1)
                send_command('s')
                scan = scan_head()
                direction = choose_direction(scan)
                send_command(direction.lower())
                time.sleep(1)
                send_command('s')
        elif frontDist >= minDist:
            send_command('f')
        if frontDist < minDist > backDist:
            send_command('s')
            print("I'm stuck!")
            for _ in range(3):
                send_command('A')
                time.sleep(0.4)

try:
    decision_loop()
except KeyboardInterrupt:
    send_command('s')
    print("Navigation manually halted.")
