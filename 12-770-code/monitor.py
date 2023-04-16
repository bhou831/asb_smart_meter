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


# Create a live chart for the voltage, current, and power
fig = make_subplots(rows=3, cols=1, specs=[[{'type': 'scatter'}],
                                           [{'type': 'scatter'}],
                                           [{'type': 'scatter'}]],
                                           row_heights=[0.33, 0.33, 0.33])

trace_voltage = go.Scatter(x=[], y=[], mode='lines+markers', name='Voltage')
trace_currentA = go.Scatter(x=[], y=[], mode='lines+markers', name='CurrentA')
trace_powerA = go.Scatter(x=[], y=[], mode='lines+markers', name='PowerA')

fig.add_trace(trace_voltage, row=1, col=1)
fig.add_trace(trace_currentA, row=2, col=1)
fig.add_trace(trace_powerA, row=3, col=1)

#increase the height
fig.update_layout(height=900)

# Create global variables for x_data and y_data
time_data = []
y_data_voltage = []
y_data_currentA = []
y_data_powerA = []

# Define an update function for the plot
def update_plot():
    global x_data_voltage, y_data_voltage, y_data_currentA, y_data_powerA
    fig.data[0].x = time_data
    fig.data[0].y = y_data_voltage
    fig.data[1].x = time_data
    fig.data[1].y = y_data_currentA
    fig.data[2].x = time_data
    fig.data[2].y = y_data_powerA


def read_data():
    global x_data, y_data
    start_time = time.time()
    for i in range(60):
        spi_bus = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        energy_sensor = ATM90e32(spi_bus, cs, lineFreq, PGAGain,
                            VoltageGain, CurrentGainCT1, 0, CurrentGainCT2)# Collect data for 60 seconds# Open the CSV file for writing
        # Read the energy data from the sensor
        voltageA = energy_sensor.line_voltageA * 120 / 640
        currentA = energy_sensor.line_currentA * 50
        powerA = energy_sensor.active_power
        
        time_data.append(time.time() - start_time) # append current time to list
        y_data_voltage.append(voltageA) # append current voltage to list
        y_data_currentA.append(currentA) # append current currentA to list
        y_data_powerA.append(powerA) # append current powerA to list


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