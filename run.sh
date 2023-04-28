#!/bin/bash

# This script will run read-value.py, terminate it after 50 minutes, and repeat this process 10 times.
# Loop 10 times
clear
python3 consume.py

num_itr=10

for i in $(seq 1.. $num_itr); do
  echo "Starting iteration $i of read-values.py"
  
  # Run read-value.py in the background and save its process ID (PID)
  python3 read-values.py
  
  # Wait for 50 minutes (3000 seconds)
  sleep 3s
done

echo "All 10 iterations completed."