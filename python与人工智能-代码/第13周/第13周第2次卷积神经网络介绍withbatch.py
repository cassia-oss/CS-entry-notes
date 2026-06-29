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
        output1 = self.nf(self.conv1(x))
        print(output1.shape)
        output1 = self.pool1(output1)
        print(output1.shape)
        output2 = self.nf(self.conv2(output1))
        print(output2.shape)
        output2 = self.pool2(output2)
        print(output2.shape)
        # Flatten
        output3 = output2.view(x.shape[0],-1)  #output3 = output2.view(-1, 400)
        print(output3.shape)
        # FC
        output3 = self.fc(output3)
        print(output3.shape)
        # SoftMax
        output = torch.softmax(output3,dim=1)
        return output

image1 = Image.open('5.jpg').convert('RGB')
input1 = transforms.ToTensor()(image1).unsqueeze(0)
image2 = Image.open('3.jpg').convert('RGB')
input2 = transforms.ToTensor()(image2).unsqueeze(0)
input = torch.cat([input1,input2],0)
print(input.shape)

model = CNN()
output = model(input)
print(output.shape)
print(output)