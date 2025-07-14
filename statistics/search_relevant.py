import csv
import sys
import os

def find_rows_by_index(csv_path, index):
    matching_rows = []
    with open(csv_path, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row and row[0] == index:
                matching_rows.append(row)
    return matching_rows

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python find_row.py <index>")
        sys.exit(1)

    index = sys.argv[1]
    csv_file = '../video_processing/output/video_data.csv'

    if not os.path.exists(csv_file):
        print(f"CSV file not found at: {csv_file}")
        sys.exit(1)

    results = find_rows_by_index(csv_file, index)
    if results:
        for row in results:
            print("Title: " + row[2])
            print("Relevant: " + row[4])
            print("URL: " + row[1])
            print("Category: " + row[3])
    else:
        print(f"No matching rows found for index: {index}")

