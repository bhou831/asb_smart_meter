import sys
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import RPi.GPIO as GPIO
import csv

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

# Create an MCP3008 object
mcp = MCP.MCP3008(spi, cs)
# Create an analog input channel on the MCP3008 pin 0
channel = AnalogIn(mcp, MCP.P0)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
red_led = 18
GPIO.setup(red_led, GPIO.OUT)

def main():
    filename = "analog.csv"
    with open(filename, 'a') as file:
        fd = csv.writer(file)
        fd.writerow(["timestamp","voltage"])
    while True:
        current_time = time.strftime("%Y-%m-%dT%H:%M:%S")

        fd.writerow([current_time,channel.voltage])
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)