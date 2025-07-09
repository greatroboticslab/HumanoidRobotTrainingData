import os
import csv
import subprocess
import json

RAW_DIR = "rawvideos"
OUTPUT_CSV = "output/video_data.csv"
YOUTUBE_PREFIX = "https://www.youtube.com/watch?v="

def get_video_data(video_id):
    try:
        # Use yt-dlp to get video metadata in JSON format
        result = subprocess.run(
            ["yt-dlp", f"https://www.youtube.com/watch?v={video_id}", "--skip-download", "--print-json", "--cookies", "cookies.txt"],
            capture_output=True, text=True, check=True
        )
        metadata = json.loads(result.stdout.strip())
        title = metadata.get("title", "Unknown Title")
        category = metadata.get("category") or (
            metadata.get("categories")[0] if "categories" in metadata and metadata["categories"] else "Unknown"
        )
        return [title.replace(",", ""), category]  # Remove commas

    except Exception as e:
        print(f"Error fetching metadata for video ID {video_id}: {e}")
        return ["Unknown Title", "Unknown Category"]

def main():
    mp3_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".mp4")]
    video_ids = [os.path.splitext(f)[0] for f in mp3_files]

    with open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["index", "url", "video title", "category", "relevant"])

        for index, video_id in enumerate(video_ids, start=1):
            url = f"{YOUTUBE_PREFIX}{video_id}"
            title, category = get_video_data(video_id)
            writer.writerow([video_id, url, title, category, "no"])
            print(f"[{index}] {video_id} → {title}")

if __name__ == "__main__":
    main()
