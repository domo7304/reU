import torch
import torch.nn as nn
import torch.nn.functional as F

import pretrainedmodels
import pretrainedmodels.utils as utils

alexnet = pretrainedmodels.__dict__['alexnet'](num_classes=1000, pretrained='imagenet')#.cuda() #pretrained model
resnet  = pretrainedmodels.__dict__['resnet18'](num_classes=1000, pretrained='imagenet')#.cuda()


class Encoder_Alex(nn.Module): #pretrained model weight
    def __init__(self):
        super(Encoder_Alex, self).__init__()
        self.encoder = alexnet._features

    def forward(self, x):
        outputs = self.encoder(x)
        return outputs


class Encoder_R18(nn.Module):

    def __init__(self):
        super(Encoder_R18, self).__init__()

        self.conv1 = resnet.conv1
        self.conv1 = resnet.conv1
        self.bn1 = resnet.bn1
        self.relu = resnet.relu
        self.maxpool = resnet.maxpool
        self.layer1 = resnet.layer1
        self.layer2 = resnet.layer2
        self.layer3 = resnet.layer3
        self.layer4 = resnet.layer4

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        outputs = self.layer4(x)
        return outputs


class MLP_Alex(nn.Module): #finetuning

    def __init__(self):
        super(MLP_Alex, self).__init__()

        self.avgpool = alexnet.avgpool
        self.linear1 = nn.Linear(9216, 256)
        self.linear2 = nn.Linear(256, 64)
        self.relu0 = alexnet.relu0
        self.relu1 = alexnet.relu1
        self.drop0 = alexnet.dropout0
        self.drop1 = alexnet.dropout0
        self.final_layer = nn.Linear(64, 4)

        self.batchnorm = nn.BatchNorm1d(64, affine=True)

    def forward(self, x):
        x = torch.flatten(self.avgpool(x), 1)
        x = self.relu0(self.linear1(self.drop0(x)))
        x = self.relu1(self.batchnorm(self.linear2(self.drop1(x))))
        outputs = self.final_layer(x)
        return outputs


class MLP_R18(nn.Module):

    def __init__(self):
        super(MLP_R18, self).__init__()

        self.avgpool = resnet.avgpool
        self.last_linear = resnet.last_linear
        self.linear1 = nn.Linear(1000, 256)
        self.linear2 = nn.Linear(256, 64)
        self.final_layer = nn.Linear(64, 4)

        self.batchnorm = nn.BatchNorm1d(64, affine=True)

    def forward(self, x):
        x = torch.flatten(self.avgpool(x), 1)
        x = self.last_linear(x)
        x = F.relu(self.linear1(F.dropout2d(x)))
        x = F.relu(self.batchnorm(self.linear2(F.dropout2d(x))))
        outputs = self.final_layer(x)
        return outputs


def encoder_alex():
    encoder = Encoder_Alex()
    return encoder
def encoder_resnet18():
    encoder = Encoder_R18()
    return encoder

def mlp_alex():
    mlp = MLP_Alex()
    return mlp
def mlp_resnet18():
    mlp = MLP_R18()
    return mlp
