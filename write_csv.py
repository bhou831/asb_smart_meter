import digitalio
import board
import busio
import time
import csv
from atm90e32 import ATM90e32
import gc
import datetime
import json
import os

with open('config.json') as file:
    configuration = json.load(file)

# Generate a timestamp string
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# ***** CALIBRATION SETTINGS *****/
lineFreq = 4485  # 4485 for 60 Hz (North America)
# 389 for 50 hz (rest of the world)
PGAGain = 21  # 21 for 100A (2x), 42 for >100A (4x)

VoltageGain = 32428 # 42080 - 9v AC transformer.
# 32428 - 12v AC Transformer

CurrentGainCT1 = 38695  # 38695 - SCT-016 120A/40mA
CurrentGainCT2 = 25498  # 25498 - SCT-013-000 100A/50mA
# 46539 - Magnalab 100A w/ built in burden resistor

RABBITMQ_HOST = configuration["HOST"]
QUEUE_NAME = configuration["QUEUE"]
FILE_PATH = configuration["FILE_PATH"]

current_lst = []
voltage_lst = []

def init_energy_sensor():
    spi_bus = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    energy_sensor = ATM90e32(spi_bus, cs, lineFreq, PGAGain, VoltageGain, CurrentGainCT1, 0, CurrentGainCT2)
    return spi_bus, cs, energy_sensor

def deinit_resources(spi_bus, cs):
    cs.deinit()
    spi_bus.deinit()

def write_to_csv():
    # Check if the file exists and has content
    file_exists = os.path.isfile(FILE_PATH) and os.path.getsize(FILE_PATH) > 0

    with open(FILE_PATH, mode='a') as csv_file:
        fieldnames = ['time', 'voltage', 'current', 'frequency', 'power']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row to the CSV file if it doesn't exist
        if not file_exists:
            writer.writeheader()

        spi_bus, cs, energy_sensor = init_energy_sensor()

        # Read the energy data from the sensor
        sys0 = energy_sensor.sys_status0
        voltage = energy_sensor.line_voltageA
        current = energy_sensor.line_currentA

        # filter out the irregular current spikes
        if len(voltage_lst) > 0 and (current > 4 or voltage < 70):
            current = current_lst[-1]
            voltage = voltage_lst[-1]

        voltage_lst.append(voltage)
        current_lst.append(current)

        # Write the energy data to the CSV file
        writer.writerow({'time': int(time.time()),
                         'voltage': voltage * 120 / 640,
                         'current': current,
                         'frequency': energy_sensor.frequency * 60 / 50,
                         'power': voltage * 120 / 640 * current})
        csv_file.flush()
        deinit_resources(spi_bus, cs)
        del energy_sensor
        gc.collect()

    # Print a message to indicate that the CSV file has been written
    print(f"Energy data saved to {FILE_PATH}")