import pandas as pd
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Helper script to calculate accuracy results.')

parser.add_argument('--filepath', help='A csv to read.', required=True)
args = parser.parse_args()
results = pd.read_csv(args.filepath)

for i in range(3):
    subset = results[results["actual"]==i]
    accuracy = len(subset[subset["prediction"]==i])/len(subset) * 100
    print(f"Accuracy for Category #{i}: {accuracy:.2f}%")
