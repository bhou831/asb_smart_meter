#!/bin/bash

# This script will run read-value.py, terminate it after 50 minutes, and repeat this process 10 times.
cd /home/proj770/asb_smart_meter
# Loop 10 times
for i in {1..5}; do
  echo "Starting iteration $i of read-value.py"
  
  # Run read-value.py in the background and save its process ID (PID)
  python3 read-value.py &
  read_value_pid=$!
  
  # Wait for 50 minutes (3000 seconds)
  sleep 30s
  
  # Terminate the read-value.py process using its PID
  echo "Terminating iteration $i of read-value.py"
  kill -2 $read_value_pid

  # Wait a bit before starting the next iteration
  sleep 5s
done

echo "All 10 iterations completed."