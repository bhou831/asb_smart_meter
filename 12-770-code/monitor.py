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
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import threading

# ***** CALIBRATION SETTINGS *****/
lineFreq = 4485  # 4485 for 60 Hz (North America)
# 389 for 50 hz (rest of the world)
PGAGain = 21  # 21 for 100A (2x), 42 for >100A (4x)

VoltageGain = 32428 # 42080 - 9v AC transformer.
# 32428 - 12v AC Transformer

CurrentGainCT1 = 38695  # 38695 - SCT-016 120A/40mA
CurrentGainCT2 = 25498  # 25498 - SCT-013-000 100A/50mA
# 46539 - Magnalab 100A w/ built in burden resistor


# Create a live chart
fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])
trace_voltage = go.Scatter(x=[], y=[], mode='lines+markers', name='Voltage')
fig.add_trace(trace_voltage)

# Create global variables for x_data and y_data
x_data = []
y_data = []

# Define an update function for the plot
def update_plot():
    global x_data, y_data
    fig.data[0].x = x_data
    fig.data[0].y = y_data


def read_data():
    global x_data, y_data
    for i in range(60):
        spi_bus = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        energy_sensor = ATM90e32(spi_bus, cs, lineFreq, PGAGain,
                            VoltageGain, CurrentGainCT1, 0, CurrentGainCT2)# Collect data for 60 seconds# Open the CSV file for writing
        # Read the energy data from the sensor
        voltageA = energy_sensor.line_voltageA
        
        x_data.append(time.time() - start_time) # append current time to list
        y_data.append(voltageA * 120 / 640) # append current voltage to list

        time.sleep(1)

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Graph(id='live-plot', figure=fig),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0) # Update every second
])

# Define the callback to update the plot
@app.callback(Output('live-plot', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_live_plot(n):
    update_plot()
    return fig

# Start a thread to read data
data_thread = threading.Thread(target=read_data)
data_thread.start()

# Run the Dash app
app.run_server(port=8080)