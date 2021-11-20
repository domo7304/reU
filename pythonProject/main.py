"""
import io
import json
import os

import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
model = models.densenet121(pretrained=True)             # ImageNet의 1000개 클래스를 학습
model.eval()                                            # autograd를 끄고 (추론만 진행할 것이기 때문에)

img_class_map = None
mapping_file_path = 'index_to_name.json'                # 사람이 읽을 수 있는 ImageNet 클래스 이름
if os.path.isfile(mapping_file_path):
    with open(mapping_file_path) as f:
        img_class_map = json.load(f)


# 전처리, 웹 요청으로 이미지 파일을 받지만, 텐서로 변환 필요
def transform_image(infile):
    # 순서대로 resize, 텐서변환, 정규화
    input_transforms = [transforms.Resize(255),         # 이미지 준비를 위해 여러 TorchVision transforms 사용
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])]
    my_transforms = transforms.Compose(input_transforms)
    image = Image.open(infile)                          # 이미지 파일 열기
    timg = my_transforms(image)                         # PIL 이미지를 적절한 모양의 PyTorch 텐서로 변환
    timg.unsqueeze_(0)                                  # PyTorch 모델은 배치 입력을 예상하므로 1짜리 배치를 만듦
    return timg


# 추론
def get_prediction(input_tensor):
    outputs = model.forward(input_tensor)               # 모든 ImageNet 클래스에 대한 가능성(likelihood) 얻기
    _, y_hat = outputs.max(1)                           # 가장 가능성 높은 클래스 추출 (첫 번째 것만 추출)
    prediction = y_hat.item()                           # PyTorch 텐서에서 int 값 추출
    return prediction


# 얻어온 클래스 인덱스에 해당하는 클래스 이름 찾아오기
def render_prediction(prediction_idx):
    stridx = str(prediction_idx)
    class_name = 'Unknown'
    if img_class_map is not None:
        if stridx in img_class_map is not None:
            class_name = img_class_map[stridx][1]

    return prediction_idx, class_name


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file is not None:
            input_tensor = transform_image(file)
            prediction_idx = get_prediction(input_tensor)
            class_id, class_name = render_prediction(prediction_idx)
            #return jsonify({'class_id': class_id, 'class_name': class_name})
            return render_template('index.html', id=class_id, name=class_name)


if __name__ == '__main__':
    app.run()
"""
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
        files = os.listdir("static/images")

        print(f.filename)

        # 파일명과 파일경로를 데이터베이스에 저장함
        sql = "INSERT INTO Image (imgname, imgDir) VALUES (%s, %s)"
        val = (secure_filename(f.filename), 'images/' + secure_filename(f.filename))
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()

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

