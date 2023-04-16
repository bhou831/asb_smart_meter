import digitalio
import board
import busio
import time
import csv
from atm90e32 import ATM90e32
from adafruit_bus_device.spi_device import SPIDevice
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

# ***** CALIBRATION SETTINGS *****/
lineFreq = 4485  # 4485 for 60 Hz (North America)
# 389 for 50 hz (rest of the world)
PGAGain = 21  # 21 for 100A (2x), 42 for >100A (4x)

VoltageGain = 32428 # 42080 - 9v AC transformer.
# 32428 - 12v AC Transformer

CurrentGainCT1 = 38695  # 38695 - SCT-016 120A/40mA
CurrentGainCT2 = 25498  # 25498 - SCT-013-000 100A/50mA
# 46539 - Magnalab 100A w/ built in burden resistor

FILE_PATH = "energy_data_4.csv"

# Create a live chart
fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])
trace_voltage = go.Scatter(x=[], y=[], mode='lines+markers', name='Voltage')
fig.add_trace(trace_voltage)
start_time = time.time()

# Define an update function for the plot
def update_plot(x_data, y_data):
    fig.update_traces(x=x_data, y=y_data, selector=dict(type='scatter'))
    pio.show(fig, auto_play=True)



for i in range(60):
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
    
    x_data = [time.time() - start_time] # append current time to list
    y_data = [voltageA*120/640] # append current voltage to list

    # Update the live plot
    update_plot(x_data, y_data)

    time.sleep(1)
        
# Print a message to indicate that the CSV file has been written
print(f"Energy data saved to {FILE_PATH}")
