import serial
import time

# Adjust the serial port as needed; often /dev/ttyACM0 or /dev/ttyUSB0
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

arduino.write(b'f')  # Send forward command
time.sleep(2)
arduino.write(b'b')  # Backward
time.sleep(2)
arduino.write(b's')  # Stop

arduino.close()
