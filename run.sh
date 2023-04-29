#!/bin/bash

clear
num_itr=30000

for i in $(seq 1 $num_itr); do
  echo "Starting iteration $i of read-values.py"
  
  python3 read-values.py
  
  sleep 3s
done

echo "All 30000 iterations completed."