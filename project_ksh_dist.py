from __future__ import print_function, division
import os

# os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
# os.environ['CUDA_VISIBLE_DEVICES'] = "0"

import torch
import pandas as pd
import numpy as np

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable
import torch.nn.functional as F

import augly.image as imaugs  # https://github.com/facebookresearch/AugLy
from models_ksh import encoder_alex, encoder_resnet18, mlp_alex, mlp_resnet18
# github link: https://github.com/Cadene/pretrained-models.pytorch


def model_training(model, optimizer, scheduler):

    # def init_weights(m):
    #     if type(m) == nn.Linear:
    #         #torch.nn.init.normal_(m)
    #         m.weight.normal_
            
    encoder = model[0]
    mlp = model[1]
    #mlp.apply(init_weights)

    enc_opt = optimizer[0]
    mlp_opt = optimizer[1]

    criterion = nn.CrossEntropyLoss()

    for epoch in range(40):

        # running_loss = 0.0
        for i, data in enumerate(loaders['train']):

            inputs, labels = data['image'], data['class']

            if use_gpu:
                inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            else:
                inputs, labels = Variable(inputs), Variable(labels)
                
            z = encoder(inputs)
            outputs = mlp(z)
            
            y_one_hot = torch.zeros_like(outputs)
            y_one_hot.scatter_(1, labels.unsqueeze(1), 1)
            loss = (y_one_hot * -torch.log(F.softmax(outputs, dim=1))).sum(dim=1).mean()
            
            # print(y_one_hot)
            # print(y_one_hot.shape)

            # loss = criterion(outputs, y_one_hot)

            enc_opt.zero_grad()
            mlp_opt.zero_grad()
            loss.backward()

            enc_opt.step()
            mlp_opt.step()

            # running_loss += loss.item()
            if i % 30 == 0:  # print every 10 epochs
                print('[%d, %5d] loss: %.3f' % (epoch + 1, i+1, loss / 32))
        
        if epoch % 5 == 0:
            PATH_encoder = 'checkpoint/project_ksh_encoder_{}.t7'.format(epoch)
            PATH_mlp     = 'checkpoint/project_ksh_mlp_{}.t7'.format(epoch)
            torch.save(encoder.state_dict(), PATH_encoder)
            torch.save(mlp.state_dict(), PATH_mlp)

        scheduler[0].step()
        scheduler[1].step()

    print('Finish Training')

    PATH_encoder = 'project_ksh_encoder_final.t7'
    PATH_mlp     = 'project_ksh_mlp_final.t7'
    torch.save(encoder.state_dict(), PATH_encoder)
    torch.save(mlp.state_dict(), PATH_mlp)


def model_evaluation(model, weights_name, dataset_size):
    
    encoder = model[0]
    mlp = model[1]

    encoder_name = weights_name[0]
    mlp_name = weights_name[1]
    
    # Check all weights
    for i in range(20):
        weight_enc_name = 'checkpoint/project_ksh_encoder_{}.t7'.format(5*i)
        weight_mlp_name = 'checkpoint/project_ksh_mlp_{}.t7'.format(5*i)
    

    encoder.load_state_dict(torch.load(encoder_name), strict=False)
    mlp.load_state_dict(torch.load(mlp_name), strict=False)

    # classes = ('can', 'disposable_cup', 'disposable_straw', 'glass', 'mugs', 'paper_cup')
    classes = ('can', 'disposable_cup', 'glass', 'mugs')
    batch_size = dataloader_val.batch_size
    evaluation_size = dataset_size['val']

    correct = 0
    reusable = 0
    non_resuable = 0
    total = evaluation_size
    with torch.no_grad():
        for i, data in enumerate(loaders['val']):
           
            inputs, labels = data['image'], data['class']  #TODO(): 이 label은 0, 1, 2...
            
            if use_gpu:
                inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            else:
                inputs, labels = Variable(inputs), Variable(labels)
            
            outputs = mlp(encoder(inputs))
            _, predicted = torch.max(outputs, 1)
            print(predicted, labels)
            
            
            correct += (predicted == labels).sum().item()
            # if len(predicted) == 5:
            #     print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(batch_size))) #test갯수만
            # else:
            print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(len(predicted))))
    print('Accuracy of the network on the sample test images: %d %%' % (
            100 * correct / evaluation_size))

    
    
def evaluate_all_weights(model, dataset_size):
    
    encoder = model[0]
    mlp = model[1]

    # Check all weights
    for w in range(20):
        weight_enc_name = 'checkpoint/project_ksh_encoder_{}.t7'.format(5*w)
        weight_mlp_name = 'checkpoint/project_ksh_mlp_{}.t7'.format(5*w)
    

        encoder.load_state_dict(torch.load(weight_enc_name), strict=False)
        mlp.load_state_dict(torch.load(weight_mlp_name), strict=False)
    
        # classes = ('can', 'disposable_cup', 'disposable_straw', 'glass', 'mugs', 'paper_cup')
        classes = ('can', 'disposable_cup', 'glass', 'mugs')
        batch_size = dataloader_val.batch_size
        evaluation_size = dataset_size['val']
    
        correct = 0
        reusable = 0
        non_resuable = 0
        total = evaluation_size
        with torch.no_grad():
            for i, data in enumerate(loaders['val']):
                
                inputs, labels = data['image'], data['class']  #TODO(): 이 label은 0, 1, 2...
                
                if use_gpu:
                    inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
                else:
                    inputs, labels = Variable(inputs), Variable(labels)
                
                outputs = mlp(encoder(inputs))
                _, predicted = torch.max(outputs, 1)
                print(predicted, labels)
                
                correct += (predicted == labels).sum().item()
                print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(len(predicted)))) #test갯수만
    
        print('Accuracy of the network (epoch {}) on the sample test images: {} %%'.format(
                w, 100 * correct / evaluation_size))
        
        
def TEST(model, weights_name):
    import os
    import matplotlib.pyplot as plt
    
    encoder = model[0]; mlp = model[1]

    encoder_name = weights_name[0]; mlp_name = weights_name[1]
    
    encoder.load_state_dict(torch.load(encoder_name), strict=False)
    mlp.load_state_dict(torch.load(mlp_name), strict=False)
    encoder.eval()
    mlp.eval()
    
    my_transforms = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(size=224),
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
                                       ])

    classes = ('can', 'disposable_cup', 'glass', 'mugs')
    
    # url = "https://dispatch.cdnser.be/cms-content/uploads/2020/04/09/a26f4b7b-9769-49dd-aed3-b7067fbc5a8c.jpg"
    #url = "http://localhost:5000/static/images/00000000.jpg"
    #url = img_path
    url = "http://localhost:5000/static/images/KakaoTalk_20211120_145754870.jpg"
    os.system("curl " + url + " > test.jpg")
    img = Image.open("test.jpg")
    plt.imshow(img)
    
    tensor = my_transforms(img).unsqueeze(0)
    outputs = mlp(encoder(tensor))
    _, y_hat = outputs.max(1)
    predicted_idx = y_hat.item()
    
    SM = torch.nn.Softmax()  # convert score to probability (0 to 1)
    confidence_score = SM(outputs).max()
    
    
    if predicted_idx > 1:
        # disposable
        print('Requested image class is "{} with confidence score {}"'.format(classes[predicted_idx], confidence_score))
        print("Disposable class: {}.".format(classes[predicted_idx]))
        print("Point +1")
    else:
        print('Requested image class is "{} with confidence score {}"'.format(classes[predicted_idx], confidence_score))
        print("Not disposable class: {}.".format(classes[predicted_idx]))
        
        


class Custom_dataloader(Dataset): #이게 핵심

    def __init__(self, csv_file, root_dir, transform=None, inFolder=None): #이미지경로, csv파일 경로, 전처리

        self.training_sheet = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        if inFolder is None:
            self.inFolder = np.full((len(self.training_sheet),), True)
        
        self.loc_list = np.where(inFolder)[0]
        self.infold = self.inFolder
        
    def __len__(self):
        return  np.sum(self.infold*1)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.training_sheet.iloc[idx, 0])
        classes = self.training_sheet.iloc[idx,1]
        # print(img_name)
        sample = Image.open(img_name)
        
        if self.transform:
            sample = self.transform(sample)
        return {'image': sample, 'class': classes}


if __name__ == "__main__":

    import warnings
    warnings.filterwarnings("ignore")
    
    use_gpu = torch.cuda.is_available()
    device = torch.device("cuda:0")
    
    training_path = '/Users/ksh76/project_ksh/datasets/training.csv'
    validation_path = '/Users/ksh76/project_ksh/datasets/validation.csv'

    project_dataset = Custom_dataloader(csv_file=training_path,
                               root_dir='/Users/ksh76/project_ksh/datasets/',
                               transform=transforms.Compose([
                                   transforms.Resize(256), transforms.RandomCrop(size=224),
                                   transforms.ColorJitter(),
                                   transforms.RandomHorizontalFlip(),
                                    #Image augmentation tools from AugLy
                                    imaugs.Brightness(factor=2.0),
                                    # imaugs.RandomRotation(),
                                    imaugs.Saturation(factor=2.0),
                                   
                                   transforms.ToTensor(),
                                   transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
                               ]), inFolder=None)

    project_dataset_val = Custom_dataloader(csv_file=validation_path,
                                   root_dir='/Users/ksh76/project_ksh/datasets/',
                                   transform=transforms.Compose([
                                       transforms.Resize(256), transforms.CenterCrop(size=224),
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
                                   ]), inFolder=None)

    
    batch_size = 32
    dataloader = DataLoader(project_dataset, batch_size=batch_size, shuffle=True)
    dataloader_val = DataLoader(project_dataset_val, batch_size=5, shuffle=False)
    
    loaders = {'train': dataloader, 'val': dataloader_val}
    dataset_size = {'train': len(project_dataset), 'val': len(project_dataset_val)}
    
    use_gpu = torch.cuda.is_available()

    encoder = encoder_alex()#.cuda()
    mlp = mlp_alex()#.cuda()

    # enc_opt = optim.Adam(encoder.parameters(), lr = 1e-4, betas = (0.5, 0.9))
    # mlp_opt = optim.Adam(mlp.parameters(), lr = 1e-4, betas = (0.5, 0.9))
    
    enc_opt = optim.SGD(encoder.parameters(), lr = 1e-2)
    mlp_opt = optim.SGD(mlp.parameters(), lr = 1e-1)
    
    enc_exp_lr_scheduler = lr_scheduler.MultiStepLR(enc_opt, milestones=[5e2,10e2,20e2,50e2,100e2], gamma=0.8)
    mlp_exp_lr_scheduler = lr_scheduler.MultiStepLR(mlp_opt, milestones=[5e2,10e2,20e2,50e2,100e2], gamma=0.8)

    # 1) Train
    model_training([encoder, mlp], [enc_opt, mlp_opt], [enc_exp_lr_scheduler , mlp_exp_lr_scheduler])
    
    
    # 2) Simple evaluation    
    # PATH_encoder = 'project_ksh_encoder_final.t7'
    # PATH_mlp = 'project_ksh_mlp_final.t7'
    # PATH_encoder = 'checkpoint/project_ksh_encoder_5.t7'
    # PATH_mlp = 'checkpoint/project_ksh_mlp_5.t7'
    # model_evaluation([encoder, mlp], [PATH_encoder, PATH_mlp], dataset_size)
    
    # # 3) Evaluate all weights (optional)
    # # evaluate_all_weights([encoder, mlp], dataset_size)
    
    # 4) REAL Test
    # PATH_encoder = 'project_ksh_encoder_final.t7'
    # PATH_mlp = 'project_ksh_mlp_final.t7'
    
    # TEST([encoder, mlp], [PATH_encoder, PATH_mlp])
