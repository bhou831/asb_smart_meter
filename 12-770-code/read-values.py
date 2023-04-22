import digitalio
import board
import busio
import time
import csv
from atm90e32 import ATM90e32
from adafruit_bus_device.spi_device import SPIDevice
import matplotlib.pyplot as plt

# ***** CALIBRATION SETTINGS *****/
lineFreq = 4485  # 4485 for 60 Hz (North America)
# 389 for 50 hz (rest of the world)
PGAGain = 21  # 21 for 100A (2x), 42 for >100A (4x)

VoltageGain = 32428 # 42080 - 9v AC transformer.
# 32428 - 12v AC Transformer

CurrentGainCT1 = 38695  # 38695 - SCT-016 120A/40mA
CurrentGainCT2 = 25498  # 25498 - SCT-013-000 100A/50mA
# 46539 - Magnalab 100A w/ built in burden resistor

# adjust the time threshold to collect data
TIME_THRESHOLD = 6400
MEASUREMENT_GRANULARITY = 3 # 3 second measurement granularity

FILE_PATH = "energy_data_2_hour.csv"

current_lst = []

with open(FILE_PATH, mode='w') as csv_file:
    fieldnames = ['time', 'voltage', 'current', 'frequency', 'power']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row to the CSV file
    writer.writeheader()

    # Loop for 60 seconds
    for i in range(TIME_THRESHOLD):
        spi_bus = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        energy_sensor = ATM90e32(spi_bus, cs, lineFreq, PGAGain,
                         VoltageGain, CurrentGainCT1, 0, CurrentGainCT2)# Collect data for 60 seconds# Open the CSV file for writing
        # Read the energy data from the sensor
        sys0 = energy_sensor.sys_status0
        voltageA = energy_sensor.line_voltageA
        voltageC = energy_sensor.line_voltageC
        if (lineFreq == 4485):  # split single phase
            totalVoltage = voltageA + voltageC
        else:
            totalVoltage = voltageA  # 220-240v

        current = energy_sensor.line_currentA
        
        # filter out the irregular current spikes
        if current > 60:
            current = current_lst[-1]
        
        current_lst.append(current)

        # Write the energy data to the CSV file
        writer.writerow({'time': i, 
                         'voltage': voltageA*120/640,
                         'current': current,
                         'frequency': energy_sensor.frequency*60/50,
                         'power': voltageA*120/640*current})

        time.sleep(MEASUREMENT_GRANULARITY)
# Print a message to indicate that the CSV file has been written
print(f"Energy data saved to {FILE_PATH}")
