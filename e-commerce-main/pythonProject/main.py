from __future__ import print_function, division
import os

# os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
# os.environ['CUDA_VISIBLE_DEVICES'] = "0"

import torch
# import pandas as pd
# import numpy as np

# from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

# import torch.nn as nn
# import torch.optim as optim
# from torch.optim import lr_scheduler
# from torch.autograd import Variable
# import torch.nn.functional as F

#import augly.image as imaugs  # https://github.com/facebookresearch/AugLy
from models_ksh import encoder_alex, encoder_resnet18, mlp_alex, mlp_resnet18
# github link: https://github.com/Cadene/pretrained-models.pytorch


def TEST(model, weights_name, file):
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
    
    print(type(file.filename))
    
    url = "http://localhost:5000/static/images/" + secure_filename(file.filename)
 
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
        

import json
import logging
import sys

from flask import Flask, render_template, request, redirect, url_for
import pymysql
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')



@app.route('/fileUpload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        # 데이터베이스 값 설정
        conn = pymysql.connect(
            host='umc.c5svq8o9wqfm.ap-northeast-2.rds.amazonaws.com',
            database='ecommerce',
            port=3306,
            user='test',
            password='1111',
            charset='utf8')
        cursor = conn.cursor()

        f = request.files['file']
        f.save('static/images/' + secure_filename(f.filename))
        

        print(f.filename)

        # 파일명과 파일경로를 데이터베이스에 저장함
        sql = "INSERT INTO Image (imgname, imgDir) VALUES (%s, %s)"
        val = (secure_filename(f.filename), 'images/' + secure_filename(f.filename))
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()

        encoder = encoder_alex()#.cuda()
        mlp = mlp_alex()#.cuda()
        
        # 4) REAL Test
        PATH_encoder = 'C:/Users/ksh76/project_ksh/project_ksh_encoder_final.t7'
        PATH_mlp = 'C:/Users/ksh76/project_ksh/project_ksh_mlp_final.t7'
        
        TEST([encoder, mlp], [PATH_encoder, PATH_mlp], f)

        return redirect(url_for("main"))



@app.route('/view', methods=['GET', 'POST'])
def view():
    # 데이터베이스 값 설정
    conn = pymysql.connect(
        host='umc.c5svq8o9wqfm.ap-northeast-2.rds.amazonaws.com',
        database='ecommerce',
        port=3306,
        user='test',
        password='1111',
        charset='utf8')
    cursor = conn.cursor()

    sql = "SELECT imgname, imgDir FROM Image"
    cursor.execute(sql)  # 메소드로 전달해 명령문을 실행
    data = cursor.fetchall()  # 실행한 결과 데이터를 꺼냄

    data_list = []

    for obj in data:  # 튜플 안의 데이터를 하나씩 조회해서
        data_dic = {  # 딕셔너리 형태로
            # 요소들을 하나씩 넣음
            'name': obj[0],
            'dir': obj[1]
        }
        data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음

    cursor.close()
    conn.close()

    return render_template('view.html', data_list=data_list)  # html을 렌더하며 DB에서 받아온 값들을 넘김


if __name__ == '__main__':     
    app.run(port=5000)
    
   


