# CONFIGURATION
ENV_NAME="whisper"
FILES=(../output/video_downloading/videos.txt ../output/video_downloading/videos_s1_${1}*.txt)   # Add paths to your .txt files here
BATCH_SIZE=15
SLEEP_BETWEEN_BATCHES=300                   # Seconds between batches
MAX_DOWNLOADS=100                      # <-- Set your max video downloads here

set -x
cd ../rawvideos

echo "YT-DLP LOG" > ../output/ytdlp_output.txt

TOTAL_DOWNLOADED=0

for URL_LIST in "${FILES[@]}"; do
    BASENAME=$(basename "$URL_LIST" .txt)
    LOG_FILE="${BASENAME}_downloaded.log"

    echo ""
    echo "Processing: $URL_LIST"
    echo "Log file: $LOG_FILE"

    touch "$LOG_FILE"

    grep -vxFf "$LOG_FILE" "$URL_LIST" > temp_remaining_"$BASENAME".txt

    while [ -s temp_remaining_"$BASENAME".txt ]; do
        if [ "$TOTAL_DOWNLOADED" -ge "$MAX_DOWNLOADS" ]; then
            echo "🚫 Reached max download limit of $MAX_DOWNLOADS videos. Stopping."
            break 2
        fi

        echo "Starting new batch for $URL_LIST..."

        REMAINING=$((MAX_DOWNLOADS - TOTAL_DOWNLOADED))
        CURRENT_BATCH_SIZE=$((REMAINING < BATCH_SIZE ? REMAINING : BATCH_SIZE))

        head -n "$CURRENT_BATCH_SIZE" temp_remaining_"$BASENAME".txt > current_batch_"$BASENAME".txt

        conda run -n "$ENV_NAME" yt-dlp --merge-output-format mp4 --cookies "../cookies.txt" -o "%(id)s.%(ext)s" -a current_batch_"$BASENAME".txt >> ../output/ytdlp_output.txt

        cat current_batch_"$BASENAME".txt >> "$LOG_FILE"
        sed -i "1,${CURRENT_BATCH_SIZE}d" temp_remaining_"$BASENAME".txt

        TOTAL_DOWNLOADED=$((TOTAL_DOWNLOADED + CURRENT_BATCH_SIZE))

        echo "Batch complete ($TOTAL_DOWNLOADED / $MAX_DOWNLOADS downloaded)."
        sleep "$SLEEP_BETWEEN_BATCHES"
    done

    echo "✅ Finished processing $URL_LIST or hit limit."
    rm -f current_batch_"$BASENAME".txt temp_remaining_"$BASENAME".txt
done

echo ""
echo "🎉 Script complete. Total videos downloaded: $TOTAL_DOWNLOADED"

echo "Beginning transcription..."

cd ..
conda run -n whisper python identify_videos.py

conda run -n whisper python masswhisper.py
