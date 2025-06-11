from PIL import Image
# this script has _heavy_ ChatGPT help - thanks!
import torchvision
import torchvision.models as models
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import ImageFolder
import torch.nn as nn
import torch.optim as optim
from torchvision.transforms import v2
import argparse

# initialize the parser
parser = argparse.ArgumentParser(description='Categorize images using finetuned ResNet.')
parser.add_argument('--model-path', help='The path to a finetuned ResNet', required=True)
parser.add_argument('--folder', help='The path to the test images', required=True)
args = parser.parse_args()

# load the model and put it in eval mode
resnet = torch.load(args.model_path)
resnet.eval()

# prepare our processing
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
transform = v2.Compose([
    v2.ToImage(),
    v2.RandomResizedCrop(size=(224, 224), antialias=True),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# load our data
train_data = ImageFolder(root=args.folder, transform = transform)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
print("prediction,actual")
# Make prediction
with torch.no_grad():
    
    for images, labels in train_loader:
        images = images.to(device)

        outputs = resnet(images)
        _, predicted = torch.max(outputs, 1)
        for prediction, actual in zip(predicted, labels):
            print(f"{prediction},{actual}")

