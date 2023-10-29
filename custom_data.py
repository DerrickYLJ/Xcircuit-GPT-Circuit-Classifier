import os
import pandas as pd
from torchvision.io import read_image
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision import transforms
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from PIL import Image


annotations_file = "data/Circuits/Circuits_labels/circuit_labels.csv"
img_dir = "data/Circuits/Circuits_Images/"
class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, image_size, transform=None, target_transform=None):
        # the data images are stored in a directory img_dir, and their labels are stored separately in a CSV file annotations_file.
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(image_size),
            transforms.ToTensor()
        ])
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(img_path).convert('RGB')
        convert_tensor = transforms.ToTensor()
        image = convert_tensor(image)
        image = self.transform(image)
        label = self.img_labels.iloc[idx, 1]
        if self.target_transform:
            label = self.target_transform(label)
        return image, label

# training_data = CustomImageDataset(annotations_file, img_dir, image_size=(256, 256))
# train_dataloader = DataLoader(training_data, batch_size=32, shuffle=True)
# # test_dataloader = DataLoader(test_data, batch_size=64, shuffle=True)

# # Display image and label.
# train_features, train_labels = next(iter(train_dataloader))
# print(f"Feature batch shape: {train_features.size()}")
# print(f"Labels batch shape: {train_labels.size()}")
# img = train_features[0].squeeze()
# label = train_labels[0]
# plt.imshow(img.permute(1, 2, 0), cmap="gray")
# plt.show()
# print(f"Label: {label}")
