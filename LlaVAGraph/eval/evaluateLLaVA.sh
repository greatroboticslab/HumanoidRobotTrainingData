# define our variables
MODELPATH=/projects/imo2d/LLaVAChartv5
IMAGEFOLDER=/home/imo2d/LLaVA/data/subset/testData


# random noise
python evaluateLLaVA.py --model-path $MODELPATH --image-folder $IMAGEFOLDER/NoiseData --output-file results/llava/randomNoise.json

# sine waves
python evaluateLLaVA.py --model-path $MODELPATH --image-folder $IMAGEFOLDER/SineData --output-file results/llava/sineWave.json

#square waves
python evaluateLLaVA.py --model-path $MODELPATH --image-folder $IMAGEFOLDER/SquareData --output-file results/llava/squareWave.json
