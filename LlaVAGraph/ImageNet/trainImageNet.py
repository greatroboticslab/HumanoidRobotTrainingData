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
parser.add_argument('--model-path', help='The path to save the finetuned ResNet', required=True)
parser.add_argument('--folder', help='The path to the train images', required=True)
parser.add_argument('--epochs', type=int, help='The number of training epochs', required=True)
args = parser.parse_args()

resnet = models.resnet50(pretrained=True)

# lots of help from here: https://ds-amit.medium.com/fine-tuning-resnet50-a-practical-guide-a5d7622a608d
# Thanks :)
# Freeze all layers
for parameter in resnet.parameters():
    parameter.requires_grad = False

# Replace the classification head
num_classes = 3
resnet.fc = torch.nn.Linear(resnet.fc.in_features, num_classes)

# Unfreeze the last block
for param in resnet.layer4.parameters():
    param.requires_grad = True

# Move to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resnet = resnet.to(device)
print(resnet)
transforms = v2.Compose(
    [
        v2.ToImage(),
        v2.RandomResizedCrop(size=(224, 224), antialias=True),
        v2.RandomHorizontalFlip(p=0.5),
        v2.ToDtype(torch.float32, scale=True),
        v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# Load datasets
train_data = ImageFolder(root=args.folder, transform=transforms)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

# Class names

criterion = nn.CrossEntropyLoss()  # Because you're doing classification
optimizer = optim.Adam(resnet.parameters(), lr=0.001)

# Training loop
for epoch in range(args.epochs):
    resnet.train()
    running_loss = 0.0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = resnet(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(train_loader):.4f}")

# save the dataset
torch.save(resnet, args.model_path)
