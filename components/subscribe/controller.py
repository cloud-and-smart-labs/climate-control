import serial
import time
import random

serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
serial_port.flush()

while True:
    num = random.randint(0, 180)
    serial_port.write(bytes(f'{num}/{num}', 'utf-8'))

    print(serial_port.readline().decode('utf-8').rstrip())

    time.sleep(2)
