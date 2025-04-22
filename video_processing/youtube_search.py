import argparse
import requests
import sys
import os

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

final_urls = []

def get_youtube_results(api_key, query, max_results):
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'videoLicense': 'creativeCommon',
        'maxResults': max_results,
        'key': api_key
    }

    response = requests.get(YOUTUBE_SEARCH_URL, params=params)

    if response.status_code != 200:
        print(f"Error fetching data for query '{query}': {response.text}")
        return []

    data = response.json()
    video_urls = [
        f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        for item in data.get('items', [])
    ]

    return video_urls

def main():
    parser = argparse.ArgumentParser(description="Search YouTube for Creative Commons videos based on search phrases from a text file.")
    parser.add_argument("--input_file", help="Path to the input file with search phrases (one per line)")
    parser.add_argument("--api_key", help="YouTube Data API v3 key")
    parser.add_argument("--max_results", type=int, default=3, help="Number of results per search phrase")

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print("Input file does not exist.")
        sys.exit(1)

    with open(args.input_file, "r", encoding="utf-8") as f:
        search_phrases = [line.strip() for line in f if line.strip()]

    for phrase in search_phrases:
        print(f"\n🔍 Search: {phrase}")
        urls = get_youtube_results(args.api_key, phrase, args.max_results)
        if urls:
            for url in urls:
                print(url)
                final_urls.append(url)
        else:
            print("No Creative Commons videos found.")

if __name__ == "__main__":
    main()
    outputFile = open("videos_s1.txt", "w")
    outString = ""
    for url in final_urls:
        outString += url + "\n"
    outputFile.write(outString)
    outputFile.close()
