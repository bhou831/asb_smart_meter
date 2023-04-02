import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

red_led = 18

GPIO.setup(red_led, GPIO.OUT)

while True:
    GPIO.output(red_led, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(red_led, GPIO.LOW)
    time.sleep(1)
    print("Red light on")