# define our variables
MODELPATH=/projects/imo2d/Llama-3.2-3B-Instruct

# random noise
python summarizeLLAMA.py --model-path $MODELPATH --conversation-file results/randomNoise.json --output-file results/randomNoise.csv --answer A

# sine waves
python summarizeLLAMA.py --model-path $MODELPATH --conversation-file results/sineWave.json --output-file results/sineWave.csv --answer B

#square waves
python summarizeLLAMA.py --model-path $MODELPATH --conversation-file results/squareWave.json --output-file results/squareWave.csv --answer C
