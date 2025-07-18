# ObbyNav (Obstacle Navigation Robot)

ObbyNav is an autonomous indoor navigation robot designed to explore environments like homes, classrooms, or hallways. Built as a cost-conscious educational tool, it demonstrates concepts in robotics, embedded systems, and basic computer vision.
# 1. Overview
ObbyNav uses a combination of sensors and logic to autonomously:
- Detect and avoid walls or obstacles
- Identify doorways using a camera and image processing
- Provide audio feedback when stuck
- Adjust direction based on sensor feedback
>The robot is built using a Raspberry Pi 4 for decision-making and an Arduino Uno R3 for low-level hardware control. The modular setup and open-source nature make it suitable for students, hobbyists, and educators.

# 2. Hardware Components
- Raspberry Pi 4 (4GB) with Pi OS Lite
- Arduino Uno R3 (Elegoo)
- 5" Touchscreen Monitor for logs and interaction
- Arducam Camera for doorway detection (mounted on front)
- 2x DC Gear Motors with differential drive
- L298N Motor Driver
- SG90 Servo Motor for head-mounted scanning
- 2x HC-SR04 Ultrasonic Sensors (front & rear)
- Active Buzzer for alerts
- Power MB V2 for additional power
- Breadboard for HC-SR04
- 10,000 mAh USB Battery Pack
>Misc: cardboard frame, hot glue, jumper wires, tape, zip ties, 9V battery

# 3. Software and Behavior
- Python 3 runs on the Pi, handling navigation logic (navbrain.py)
- Arduino C++ (motors.ino) receives commands via serial and operates motors, buzzer, and servo
- Serial communication (USB) bridges the Pi and Arduino
- OpenCV is used to detect doorways based on vertical lines in images
- Head scans gather left, center, and right distance readings to determine the best path
## Behavior Overview:
- Continuously checks for obstacles using ultrasonic sensors
- If something is close in front, it pauses and attempts to identify a doorway using camera
- If a door is found, it proceeds forward; otherwise, it backs up and scans left, right, and center directions
- The robot chooses the direction with most distance and adjusts its course
>If boxed in or stuck, it beeps and will attempt to move again (in case the problem is resolved manually)
## Doorway Detection
Captured frames are processed to:
- Apply grayscale, blur, and edge detection
- Use Hough Transform to find vertical lines
- Look for parallel pairs of vertical lines representing a doorway
- If found, the area is highlighted and logged
>Images are saved with filenames like door_YYYYMMDD_HHMMSS.jpg.

# 4. Testing and Integration
The robot has been tested in multiple real-world layouts, including narrow hallways and door thresholds. Challenges such as camera angle, vibration, and power stability were solved via:
- Repositioning camera and rotating image in software
- Securing components with zip ties and tape for consistent operation
- Adding delays in Python for proper sensor timing

>If the Python script sends commands too quickly for the Arduino to process, it may cause hardware glitches such as stunted movement or missed sensor readings.

# 5. File Summary
- `navbrain.py`: Main navigation script that includes image processing.
- `README.md`: This file.
- `pi/startup.sh`: Startup script that automatically runs the python file after updating to the newest version.
- `motors/motors.ino`: Arduino motor and sensor controller.