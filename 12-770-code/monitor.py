import digitalio
import board
import busio
import time
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
from msg import send_msg
import gc

# ***** CALIBRATION SETTINGS *****/
lineFreq = 4485  # 4485 for 60 Hz (North America)
# 389 for 50 hz (rest of the world)
PGAGain = 21  # 21 for 100A (2x), 42 for >100A (4x)

VoltageGain = 32428 # 42080 - 9v AC transformer.
# 32428 - 12v AC Transformer

CurrentGainCT1 = 38695  # 38695 - SCT-016 120A/40mA
CurrentGainCT2 = 25498  # 25498 - SCT-013-000 100A/50mA
# 46539 - Magnalab 100A w/ built in burden resistor

OBSERVATION_TIME = 28800 # 120 minutes observation time
MEASUREMENT_GRANULARITY = 4 # 4 second measurement granularity
PORT = 8080 # port for the web server, default is 8080

# ***** DASH APP *****/
# Create a live chart for the voltage, current, and power
fig = make_subplots(rows=3,
                    cols=1,
                    specs=[[{'type': 'scatter'}],
                           [{'type': 'scatter'}],
                           [{'type': 'scatter'}]],
                    row_heights=[0.33, 0.33, 0.33])

trace_voltage = go.Scatter(x=[],
                           y=[],
                           mode='lines+markers',
                           name='Voltage')

trace_currentA = go.Scatter(x=[],
                            y=[],
                            mode='lines+markers',
                            name='Current')

trace_powerA = go.Scatter(x=[],
                          y=[],
                          mode='lines+markers',
                          name='Active Power')

fig.add_trace(trace_voltage,
              row=1,
              col=1)

fig.add_trace(trace_currentA,
              row=2,
              col=1)

fig.add_trace(trace_powerA,
              row=3,
              col=1)

#increase the height
fig.update_layout(height=1080)

# Create global variables for x_data and y_data
time_data = []
y_data_voltage = []
y_data_current = []
y_data_power = []

# initialize the energy sensor
def init_energy_sensor():
    spi_bus = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    energy_sensor = ATM90e32(spi_bus, cs, lineFreq, PGAGain, VoltageGain, CurrentGainCT1, 0, CurrentGainCT2)
    return spi_bus, cs, energy_sensor

# deinitialize the energy sensor
def deinit_resources(spi_bus, cs):
    cs.deinit()
    spi_bus.deinit()

# Define an update function for the plot
def update_plot():
    global time_data, y_data_voltage, y_data_current, y_data_power
    fig.data[0].x = time_data
    fig.data[0].y = y_data_voltage
    fig.data[1].x = time_data
    fig.data[1].y = y_data_current
    fig.data[2].x = time_data
    fig.data[2].y = y_data_power

# Read data from the sensor during OBSERVATION_TIME
def read_data():
    global time_data, y_data_voltage, y_data_current, y_data_power
    start_time = time.time()
    for i in range(OBSERVATION_TIME):
        # Create the energy sensor object and initialize it
        spi_bus, cs, energy_sensor = init_energy_sensor()

        # Read the energy data from the sensor, apply calibration, and append to list
        voltage = energy_sensor.line_voltageA * 120 / 640
        current = energy_sensor.line_currentA
        power = voltage * current

        # Error handling for when the sensor returns bad data
        if (voltage < 70 or current > 3) and len(y_data_voltage) > 0:
            voltage = y_data_voltage[-1]
            current = y_data_current[-1]
            power = voltage * current
        
        time_data.append(time.time() - start_time)
        y_data_voltage.append(voltage)
        y_data_current.append(current)
        y_data_power.append(power)

        # if current > 3:
        #     send_msg()

        deinit_resources(spi_bus, cs)
        # Wait for 3 second
        # del energy_sensor
        # gc.collect()
        time.sleep(MEASUREMENT_GRANULARITY)

# Create the Dash app
app = dash.Dash(__name__)

# Define the hteml layout
app.layout = html.Div([
    dcc.Graph(id='live-plot',
              figure=fig),

    dcc.Interval(id='interval-component',
                 interval=1000,
                 n_intervals=0) # Update every second
])

# Define the callback to update the plot
@app.callback(Output('live-plot', 'figure'),
              [Input('interval-component', 'n_intervals')])

# Define the update function
def update_live_plot(n):
    update_plot()
    return fig

# Start a thread to read data
data_thread = threading.Thread(target=read_data)
data_thread.start()

# Run the Dash app
app.run_server(port=PORT)