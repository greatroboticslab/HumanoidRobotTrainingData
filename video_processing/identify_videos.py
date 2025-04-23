import os
import csv
import subprocess
import json

RAW_DIR = "rawvideos"
OUTPUT_CSV = "video_data.csv"
YOUTUBE_PREFIX = "https://www.youtube.com/watch?v="

def get_video_title(video_id):
    try:
        # Use yt-dlp to get video metadata in JSON format
        result = subprocess.run(
            ["yt-dlp", f"https://www.youtube.com/watch?v={video_id}", "--skip-download", "--print", "%j"],
            capture_output=True, text=True, check=True
        )
        metadata = json.loads(result.stdout.strip())
        title = metadata.get("title", "Unknown Title")
        return title.replace(",", "")  # Remove commas
    except Exception as e:
        print(f"Error fetching metadata for video ID {video_id}: {e}")
        return "Unknown Title"

def main():
    mp3_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".mp3")]
    video_ids = [os.path.splitext(f)[0] for f in mp3_files]

    with open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["NUMBER", "URL", "video title"])

        for index, video_id in enumerate(video_ids, start=1):
            url = f"{YOUTUBE_PREFIX}{video_id}"
            title = get_video_title(video_id)
            writer.writerow([index, url, title])
            print(f"[{index}] {video_id} → {title}")

if __name__ == "__main__":
    main()
