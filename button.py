import RPi.GPIO as GPIO
import time
import sys
import csv
from datetime import datetime

GPIO.setmode(GPIO.BCM)

red_led = 18
button = 24

GPIO.setup(button, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)

filename = "buttonpresses.csv"
# Write header row only if the file is empty or does not exist
try:
    with open(filename, 'r') as file:
        pass
except FileNotFoundError:
    with open(filename, 'a') as file:
        fd = csv.writer(file)
        fd.writerow(["Timestamp", "ButtonValue"])

def main():
    previous_state = None
    while True:
        button_state = GPIO.input(button)
        if button_state != previous_state:
            with open(filename, 'a') as file:
                fd = csv.writer(file)
                timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                fd.writerow([timestamp, button_state])
                
            if button_state:
                GPIO.output(red_led, GPIO.LOW)
                print('light off')
            else:
                GPIO.output(red_led, GPIO.HIGH)
                print('light on')

            previous_state = button_state
            time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)