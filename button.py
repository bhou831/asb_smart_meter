import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

red_led = 18
button = 25

GPIO.setup(button, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)

def main():
    while True:
        if GPIO.input(button):
            GPIO.output(red_led, GPIO.LOW)
        else:
            GPIO.output(red_led, GPIO.HIGH)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)