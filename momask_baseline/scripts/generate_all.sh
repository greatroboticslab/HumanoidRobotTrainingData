# Set the maximum value for s
MAX=1000  # Change this to your desired maximum value

# Starting values
s=0
f=0

while [ $f -lt $MAX ]; do
    f=$((s + 100))
    echo "Submitting Jobs: $s - $f"
    sbatch generate_motions.slurm "$s" "$f"
    s=$((s + 100))
done
