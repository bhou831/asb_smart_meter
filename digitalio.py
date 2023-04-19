import digitalio
import board
import busio

from atm90e32 import ATM90e32
from adafruit_bus_device.spi_device import SPIDevice
# ***** CALIBRATION SETTINGS *****/
# These settings work for my setup: 
# - the SCT-013-000 CT 
# - house in North America.
# - using a 9V AC Transformer.
# ********************************/

lineFreq = 4485             # 4485 for 60 Hz (North America)
                            # 389 for 50 hz (rest of the world)
PGAGain = 21                # 21 for 100A (2x), 42 for >100A (4x)

VoltageGain = 42080         # 42080 - 9v AC transformer.
                            # 32428 - 12v AC Transformer

CurrentGainCT1 = 25498      # 38695 - SCT-016 120A/40mA CT
CurrentGainCT2 = 25498      # 25498 - SCT-013-000 100A/50mA CT
                            # 46539 - Magnalab 100A w/ built in burden resistor

###########################################################
# Initialize SPI and grab an instance of the ATM90e32 class.
###########################################################
spi_bus = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D10)
energy_sensor = ATM90e32(spi_bus, cs, lineFreq, PGAGain,
                         VoltageGain, CurrentGainCT1, 0, CurrentGainCT2)
###########################################################
# Hello, hello...can you hear me??
###########################################################
sys0 = energy_sensor.sys_status0
if (sys0 == 0xFFFF or sys0 == 0):
    print('ERROR: not receiving data from the energy meter')
############################################################
# Print out the amount of power being used.
############################################################    
print('Active Power: {}W'.format(energy_sensor.active_power))
############################################################
# Print out voltage, current, and frequency readings.
############################################################
print('Voltage 1: {}V'.format(energy_sensor.voltageA))
print('Voltage 2: {}V'.format(energy_sensor.voltageC))
print('Current 1: {}A'.format(energy_sensor.line_currentA))
print('Current 2: {}A'.format(energy_sensor.line_currentC))
print('Frequency: {}Hz'.format(energy_sensor.frequency))