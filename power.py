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
# Create analog input channels on the MCP3008 pin 0 for voltage and pin 1 for current
voltage_channel = AnalogIn(mcp, MCP.P0)
current_channel = AnalogIn(mcp, MCP.P1)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
red_led = 22
GPIO.setup(red_led, GPIO.OUT)

# Function to convert raw ADC value to current (mA) using ACS712 sensor
def adc_to_current(adc_value, sensitivity=66):  # sensitivity in mV/A, default for ACS712 20A
    voltage = (adc_value * 3.3) / 65535  # Convert ADC value to voltage
    current = (voltage - 1.65) * 1000 / sensitivity  # Calculate current in mA
    return current

def main():
    filename = "power.csv"
    
    while True:
        current_time = time.strftime("%Y-%m-%dT%H:%M:%S")

        voltage = voltage_channel.voltage
        current = adc_to_current(current_channel.value)
        power = voltage * current / 1000  # Calculate power in watts (W)

        with open(filename, 'a') as file:
            fd = csv.writer(file)
            if file.tell() == 0:  # Check if the file is empty
                fd.writerow(["timestamp", "voltage", "current", "power"])
            fd.writerow([current_time, voltage, current, power])

        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)