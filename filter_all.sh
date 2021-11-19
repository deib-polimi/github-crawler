#!/bin/bash

mkdir -p results-filtered
for filepath in results/*.csv
do
  filename=$(basename $filepath)
  echo "Processing $filename"
  python filter.py -s 10 -c 2021-10-01 -i results/$filename -o results-filtered/$filename
  echo "Sleeping..."
  sleep 30
done