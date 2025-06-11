# define our variables
MODELPATH=/projects/imo2d/Llama-3.2-3B-Instruct

# random noise
python categorizeLLAMA.py --model-path $MODELPATH --conversation-file results/llava/randomNoise.json --output-file results/randomNoise.json

# sine waves
python categorizeLLAMA.py --model-path $MODELPATH --conversation-file results/llava/sineWave.json --output-file results/sineWave.json

#square waves
python categorizeLLAMA.py --model-path $MODELPATH --conversation-file results/llava/squareWave.json --output-file results/squareWave.json
