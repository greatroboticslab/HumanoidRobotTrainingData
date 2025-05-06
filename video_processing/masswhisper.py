from os import listdir
from os.path import isfile, join
import csv
import os
import whisper

def get_video_csv_info(mp3_filename, column_index, csv_file="output/video_data.csv"):
    # Strip the extension to get the video ID
    video_id = os.path.splitext(mp3_filename)[0]
    target_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header

            for row in reader:
                if len(row) > 1 and row[1] == target_url:
                    return row[column_index]

        print(f"Video ID '{video_id}' not found in CSV.")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None


mypath = "rawvideos/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

id = 1
model = whisper.load_model("turbo")

for file in onlyfiles:
    if(file[-3:] == "mp4"):
        v_id = os.path.splitext(file)[0]
        print("Transcribing file: " + file)
        _url = get_video_csv_info(file, 1)
        _vname = get_video_csv_info(file, 2)
        _category = get_video_csv_info(file, 3)
        if len(_category) < 3:
            _category = "Unknown Category"
        result = ""
        result += _vname + "\n"
        result += _url + "\n"
        result += _category + "\n"
        result += str(model.transcribe(mypath + file)["text"])
        file = open("transcripts/" + str(v_id) + ".txt", "w")
        file.write(result)
        file.close()

        id += 1
