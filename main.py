from __future__ import print_function, division

import torch
from torchvision import transforms
from PIL import Image
from models_ksh import encoder_alex, mlp_alex
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt


def predict(model, weights_name, file):

    encoder = model[0]
    mlp = model[1]

    encoder_name = weights_name[0]
    mlp_name = weights_name[1]

    encoder.load_state_dict(torch.load(encoder_name), strict=False)
    mlp.load_state_dict(torch.load(mlp_name), strict=False)
    encoder.eval()
    mlp.eval()

    my_transforms = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(size=224),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
                                        ])

    classes = ('can', 'disposable_cup', 'glass', 'mugs')

    img = Image.open(file['imgDir'])
    plt.imshow(img)

    tensor = my_transforms(img).unsqueeze(0)
    outputs = mlp(encoder(tensor))
    _, y_hat = outputs.max(1)
    predicted_idx = y_hat.item()

    SM = torch.nn.Softmax()  # convert score to probability (0 to 1)
    confidence_score = SM(outputs).max()

    if predicted_idx < 1:
        # disposable
        print('Requested image class is "{} with confidence score {}"'.format(classes[predicted_idx], confidence_score))
        print("Disposable class: {}.".format(classes[predicted_idx]))
    else:
        print('Requested image class is "{} with confidence score {}"'.format(classes[predicted_idx], confidence_score))
        print("Not disposable class: {}.".format(classes[predicted_idx]))

    return jsonify({
        'imgname': file['imgname'],
        'imgDir': file['imgDir'],
        'imgClass': classes[predicted_idx]
    })


app = Flask(__name__)


@app.route('/fileUpload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':

        file = request.get_json()
        encoder = encoder_alex()  # .cuda()
        mlp = mlp_alex()  # .cuda()
        path_encoder = 'project_ksh_encoder_final.t7'
        path_mlp = 'project_ksh_mlp_final.t7'

        return predict([encoder, mlp], [path_encoder, path_mlp], file)


if __name__ == '__main__':
    app.run(port=5000)




