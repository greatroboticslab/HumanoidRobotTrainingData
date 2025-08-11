#!/bin/bash

cd ..

# Set the maximum value for s
MAX=$(find ../relevantvideos/ -type f | wc -l)

# Starting values
s=0
f=0

cd scripts

while [ $f -lt $MAX ]; do
    f=$((s + 100))
    echo "Submitting Jobs: $s - $f"
    sbatch extract_frames.slurm "$s" "$f"
    s=$((s + 100))
done

