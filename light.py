import RPi.GPIO as GPIO
import time
import sys
import csv

button = 25

# Set parameters for GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN)

filename = "buttonpresses.csv"
with open(filename, 'a') as file:
    fd = csv.writer(file)
    w.writerow("Timestamp, ButtonValue")

    

def main():
    while True:
        GPIO.output(red_led, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(red_led, GPIO.LOW)
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)