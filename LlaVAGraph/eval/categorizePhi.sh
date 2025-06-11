# define our variables
MODELPATH=/projects/imo2d/phi-3.5-mini-instruct

# random noise
python categorizePhi.py --model-path $MODELPATH --conversation-file results/llava/randomNoise.json --output-file results/randomNoise.json

# sine waves
python categorizePhi.py --model-path $MODELPATH --conversation-file results/llava/sineWave.json --output-file results/sineWave.json

#square waves
python categorizePhi.py --model-path $MODELPATH --conversation-file results/llava/squareWave.json --output-file results/squareWave.json
