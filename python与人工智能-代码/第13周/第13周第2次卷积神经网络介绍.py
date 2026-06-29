import torch
import torch.nn as nn
import numpy as np
from PIL import Image
from torchvision import transforms
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3,out_channels=6,kernel_size=5,stride=1,padding=0)
        self.pool1 = nn.MaxPool2d((2,2),stride=2,padding=0)
        self.conv2 = nn.Conv2d(in_channels=6,out_channels=16,kernel_size=5,stride=1,padding=0)
        self.pool2 = nn.MaxPool2d((2,2),stride=2,padding=0)
        self.fc = nn.Linear(400,10)
        self.nf = nn.ReLU()

    def forward(self, x):
        print("x.shape = ",  x.shape)
        output1 = self.nf(self.conv1(x))
        print("after conv1 =  ", output1.shape)
        output1 = self.pool1(output1)
        print("after poo1 =  ",output1.shape)
        output2 = self.nf(self.conv2(output1))
        print("after conv2 =  ", output2.shape)
        output2 = self.pool2(output2)
        print("after poo2 =  ", output2.shape)
        # Flatten
        output3 = output2.view(1,-1)
        print("after flatten =  ", output3.shape)
        # FC
        output3 = self.fc(output3)
        print("after linear transformation = ", output3.shape)
        # SoftMax
        output = torch.softmax(output3,dim=1)
        return output

image = Image.open('5.jpg').convert('RGB')
input = transforms.ToTensor()(image).unsqueeze(0)
print("input.shape", input.shape)

model = CNN()
output = model(input)
print(output)

for parameter in model.parameters():
    print(parameter.shape)