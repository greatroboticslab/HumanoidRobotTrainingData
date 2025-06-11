> results/random-noise-experiment.txt
> results/sine-wave-experiment.txt
> results/square-wave-experiment.txt

n=10


for file in $(ls /data/isaiah/LLaVAImages/LaserData/subset/testData/NoiseData/ | tail -n $n); do
	echo $file >> results/random-noise-experiment.txt
	python llava/serve/eval.py --image-file /data/isaiah/LLaVAImages/LaserData/subset/testData/NoiseData/$file --model-path /data/isaiah/LLaVAChartv2 >> results/random-noise-experiment.txt
done

for file in $(ls /data/isaiah/LLaVAImages/LaserData/subset/testData/SineData/ |  tail -n $n); do
	echo $file >> results/sine-wave-experiment.txt
	python llava/serve/eval.py --image-file /data/isaiah/LLaVAImages/LaserData/subset/testData/SineData/$file --model-path /data/isaiah/LLaVAChartv2 >> results/sine-wave-experiment.txt
done

for file in $(ls /data/isaiah/LLaVAImages/LaserData/subset/testData/SquareData/ |tail -n $n); do
	echo $file >> results/square-wave-experiment.txt
	python llava/serve/eval.py --image-file /data/isaiah/LLaVAImages/LaserData/subset/testData/SquareData/$file --model-path /data/isaiah/LLaVAChartv2 >> results/square-wave-experiment.txt
done
