#!/bin/bash

clear
num_itr=40000

for i in $(seq 1 $num_itr); do
  echo "Starting iteration $i of write-csv.py"
  
  python3 write_csv.py
  
  sleep 3s
done

echo "All 40000 iterations completed."