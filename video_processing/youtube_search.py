import argparse
import requests
import sys
import os
import time

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

indexList = []  # Track unique video IDs
final_urls = []
urlCount = 0
maxUrls = 0
downloadedVideos = 0
lastTermLine = 0

def get_unique_youtube_results(api_key, query, target_count=10):
    global urlCount
    global downloadedVideos
    global lastTermLine
    unique_urls = []
    page_token = None

    while len(unique_urls) < target_count:
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'videoLicense': 'creativeCommon',
            'maxResults': 50,
            'key': api_key
        }

        if page_token:
            params['pageToken'] = page_token

        response = requests.get(YOUTUBE_SEARCH_URL, params=params)

        if response.status_code != 200:
            print(f"Error fetching data for query '{query}': {response.text}")
            break

        data = response.json()
        items = data.get('items', [])
        if not items:
            break

        for item in items:
            video_id = item['id']['videoId']
            if maxUrls <= 0 or (urlCount < maxUrls):
                if video_id not in indexList:
                    indexList.append(video_id)
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    unique_urls.append(url)
                    urlCount += 1
                    downloadedVideos += 1
                    print("Added url #" + str(urlCount))
                else:
                    print("Skipping duplicate: " + video_id + "...")
            else:
                break

            if len(unique_urls) >= target_count:
                break

        page_token = data.get('nextPageToken')
        if not page_token:
            break

        # Respect API rate limits
        time.sleep(1.5)

    return unique_urls

def main():
    
    global maxUrls
    global urlCount
    global lastTermLine

    parser = argparse.ArgumentParser(description="Search YouTube for Creative Commons videos based on search phrases from a text file.")
    parser.add_argument("--input_file", help="Path to the input file with search phrases (one per line)")
    parser.add_argument("--api_key", help="YouTube Data API v3 key")
    parser.add_argument("--files", type=int, default=1, help="Number of files to split the output to.")
    parser.add_argument("--max_urls", type=int, default=0, help="Maximum number of URLs to gather, set to 0 for no limit.")
    parser.add_argument("--start", type=int, default=0, help="What line in the search term file to start from. Useful for continuing from where you left off.")

    args = parser.parse_args()
    maxUrls = args.max_urls

    if not os.path.isfile(args.input_file):
        print("Input file does not exist.")
        sys.exit(1)

    # Get the existing videos
    mp4_files = [f for f in os.listdir("rawvideos") if f.endswith(".mp4")]
    for i in range(len(mp4_files)):
        mp4_files[i] = mp4_files[i][:-4]
    indexList = mp4_files

    with open(args.input_file, "r", encoding="utf-8") as f:
        search_phrases = [line.strip() for line in f if line.strip()]

    search_phrases = search_phrases[args.start:]

    for phrase in search_phrases:
        if maxUrls <= 0 or (urlCount < maxUrls):
            print(f"\n🔍 Search: {phrase}")
            urls = get_unique_youtube_results(args.api_key, phrase, target_count=10)
            lastTermLine += 1
            if urls:
                for url in urls:
                    print(url)
                    final_urls.append(url)
            else:
                print("No Creative Commons videos found.")
        else:
            break

    os.makedirs("output/video_downloading", exist_ok=True)

    #Split URLs
    split_urls = []
    ix = 0
    currentList = []
    for i in range(len(final_urls)):
        currentList.append(final_urls[i])
        ix += 1
        if ix > len(final_urls)/args.files:
            split_urls.append(currentList)
            currentList = []
            ix = 0
    if len(currentList) > 0:
        split_urls.append(currentList)

    print(split_urls)

    # Generate files
    for f in range(args.files):
        outputFile = open("output/video_downloading/videos_s1_"+str(f)+".txt", "w")
        outputFile.write("\n".join(split_urls[f]))
        outputFile.close()

    # Print info
    os.makedirs("logs", exist_ok=True)
    outputLine = "Last line: " + str(lastTermLine) + "/" + str(len(search_phrases))
    print(outputLine)
    infoFile = open("logs/lastline.txt", "w")
    infoFile.write(outputLine)
    infoFile.close()

if __name__ == "__main__":
    main()

