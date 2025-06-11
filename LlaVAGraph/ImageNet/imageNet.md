
# Comparison for ImageNet

Well, it doesn't look terrible compared to our other models.

```
python trainImageNet.py --epochs 10 --folder /home/imo2d/LLaVA/data/subset/trainData --model_path resnet_50.pth
python predictImageNet.py --folder /home/imo2d/LLaVA/data/subset/testData --model_path resnet_50.pth > results.csv
python calculateAccuracy.py --filepath results.csv
```

Results for Resnet 50 and 10 epochs:

```
Accuracy for Category #0: 100.00%
Accuracy for Category #1: 96.34%
Accuracy for Category #2: 96.25%
```

Current results for Resnet 18 and 10 epochs:

```
Accuracy for Category #0: 100.00%
Accuracy for Category #1: 95.12%
Accuracy for Category #2: 77.92%
```

Maybe LLaVAGraph isn't as terrible as it could be...
