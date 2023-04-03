import RPi.GPIO as GPIO
import time
import sys
import csv

GPIO.setmode(GPIO.BCM)

red_led = 18
button = 24

GPIO.setup(button, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)

filename = "buttonpresses.csv"
with open(filename, 'a') as file:
    fd = csv.writer(file)
    fd.writerow("Timestamp, ButtonValue")

def main():
    while True:
        if GPIO.input(button):
            GPIO.output(red_led, GPIO.LOW)
            print('light off')
        else:
            GPIO.output(red_led, GPIO.HIGH)
            print('light on')
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)