import pandas as pd
from datetime import datetime, timedelta
import pytz

# Define the time zone for the timestamps
timezone = pytz.UTC

# Load the power data into a pandas DataFrame
power_data = pd.read_csv('sample_data/fridge_207.csv')

# Set a threshold for the compressor's power consumption
compressor_threshold = 10.0

# Find the on and off times of the compressor
compressor_on = None
compressor_off = None
compressor_running = False
compressor_running_time = timedelta(0)
last_off_time = None

# Lists to store the on/off times and durations
on_times = []
off_times = []
running_durations = []
off_durations = []

for i, row in power_data.iterrows():
    # Convert the timestamp string to a datetime object
    timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))

    if row['power'] > compressor_threshold:
        if not compressor_running:
            compressor_on = timestamp.replace(tzinfo=timezone)
            compressor_running = True
            if last_off_time is not None and compressor_on is not None:
                off_duration = compressor_on - last_off_time
                off_duration_str = str(off_duration // timedelta(hours=1)) + ":" + \
                       str((off_duration % timedelta(hours=1)) // timedelta(minutes=1)).zfill(2) + ":" + \
                       str((off_duration % timedelta(minutes=1)).seconds).zfill(2)
                off_durations.append(off_duration_str)
        compressor_running_time += timedelta(seconds=1)
    else:
        if compressor_running:
            compressor_off = timestamp.replace(tzinfo=timezone)
            compressor_running = False
            
            # Convert the durations to hours:minutes:seconds format
            running_duration_str = str(compressor_running_time // timedelta(hours=1)) + ":" + \
                       str((compressor_running_time % timedelta(hours=1)) // timedelta(minutes=1)).zfill(2) + ":" + \
                       str((compressor_running_time % timedelta(minutes=1)).seconds).zfill(2)

            # Append the on/off times and durations to the lists
            on_times.append(compressor_on)
            off_times.append(compressor_off)
            running_durations.append(running_duration_str)
            
            # Store the current off time as the last off time for the next cycle
            last_off_time = compressor_off
            
            # Reset the running time counter
            compressor_running_time = timedelta(0)

# # Create a DataFrame to store the on/off times, durations, and off durations
# event_df = pd.DataFrame({'On Time': on_times, 'Off Time': off_times, 'Running Duration': running_durations, 'Off Duration': off_durations})

# # Write the DataFrame to a CSV file
# event_df.to_csv('compressor_events_317.csv', index=False)
# Create a list of tuples containing the on/off times, durations, and off durations
data = list(zip(on_times, off_times, running_durations, off_durations))

# Create a DataFrame from the list of tuples
event_df = pd.DataFrame(data, columns=['On Time', 'Off Time', 'Running Duration', 'Off Duration'])

# Write the DataFrame to a CSV file
event_df.to_csv('sample_data/event_data_207.csv', index=False)