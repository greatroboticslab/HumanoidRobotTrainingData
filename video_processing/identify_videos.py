import yt_dlp

titles = []
_urls = []

def print_youtube_titles(file_path, cookies_file='cookies.txt'):
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]

        ydl_opts = {
            'quiet': True,
            'cookiefile': cookies_file,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                try:
                    info = ydl.extract_info(url, download=False)
                    #print(f"Title: {info.get('title', 'N/A')}")
                    titles.append(str(info.get('title', 'N/A')))
                    _urls.append(url)
                except Exception as e:
                    print(f"Failed to fetch title for {url}: {e}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")

# Example usage
if __name__ == "__main__":
    file_path = "videos.txt"  # update as needed
    print_youtube_titles(file_path)
    csv_text = "id, url, name\n"
    for i in range(len(_urls)):
        csv_text += str(i) + ", " + _urls[i] + ", " + titles[i] + "\n"
    csvFile = open("rawvideos/videos.csv", "w")
    csvFile.write(csv_text)
    csvFile.close()

    #Do S1 Videos
    _urls = []
    titles = []
    file_path = "videos_s1.txt"
    print_youtube_titles(file_path)
    csv_text = "id, url, name\n"
    for i in range(len(_urls)):
        csv_text += str(i) + ", " + _urls[i] + ", " + titles[i] + "\n"
    csvFile = open("rawvideos/videos_s1.csv", "w")
    csvFile.write(csv_text)
    csvFile.close()
