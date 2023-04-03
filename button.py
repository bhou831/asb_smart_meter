import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

red_led = 18
button = 24

GPIO.setup(button, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)

def main():
    while True:
        if GPIO.input(button):
            GPIO.output(red_led, GPIO.LOW)
            print('light off')
        else:
            GPIO.output(red_led, GPIO.HIGH)
            print('light on')
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)