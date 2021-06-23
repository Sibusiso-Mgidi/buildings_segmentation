import os
import base64
import json
import requests
import io
from flask import Flask,render_template,request,redirect,flash,jsonify

import numpy as np
import cv2 as cv
from skimage import img_as_float32
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf

from metrics import get_iou_score

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No image')
            return redirect(request.url)
        elif 'mask' not in request.files:
            flash('No mask')
            return redirect(request.url)

        image_file = request.files["image"]
        mask_file = request.files['mask']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        elif mask_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        pred_image_str_1 = ''
        pred_image_str_2 = ''
        pred_image_1 =np.array([])
        pred_image_2 = np.array([])
        

        if image_file:

            pred_image_str_1,pred_image_str_2,pred_image_1,pred_image_2  = prediction(image_file)

        iou_1=0
        iou_2=0
        if mask_file:
            mask = get_mask(mask_file)
            iou_1 = get_iou_score(mask,pred_image_1)
            iou_2 = get_iou_score(mask,pred_image_2)
            
        # result = {
        #     'pred_image_1':pred_image_str_1,
        #     'pred_image_2':pred_image_str_1
        # }
        result = {
            'pred_image_1':pred_image_str_1,
            'iou_1':iou_1,
            'pred_image_2':pred_image_str_1,
            'iou_2':iou_2,
        }

        return jsonify(result)
            
    return render_template('predict.html')


def prediction(image_file):
    """
    This function takes the input image and makes a prediction of the 
    semantic segmentation of the image.
    returns: the output from two different models
    """

    # Preprocessing the input image
    image = cv.imdecode(np.fromstring(image_file.read(), np.uint8), cv.IMREAD_COLOR)
    # downsample the input image to 512 x 512 x 3
    image = cv.resize(image, (512,512))

    payload = {
        "instances": [{'input_image': image.tolist()}]
    }

    # Model one
    r_1 = requests.post('http://localhost:9000/v1/models/Segmentation:predict', json=payload)
    pred_1 = json.loads(r_1.content.decode('utf-8'))     

    # Model two
    r_2 = requests.post('http://localhost:9002/v1/models/Segmentation2:predict', json=payload)
    pred_2 = json.loads(r_2.content.decode('utf-8')) 

    pred_image_1 = np.squeeze( np.array(pred_1['predictions'])[0] > 0.5 )
    pred_image_1 = pred_image_1.astype(np.uint8)

    pred_image_2 = np.squeeze( np.array(pred_2['predictions'])[0] > 0.5 )
    pred_image_2 = pred_image_2.astype(np.uint8)

    # Convert image to base64
    plt.imshow(pred_image_1,cmap="gray")
    plt.axis("off")
    my_stringIObytes_1 = io.BytesIO()
    plt.savefig(my_stringIObytes_1, format='png',bbox_inches="tight")
    my_stringIObytes_1.seek(0)
    pred_image_b64_1 = base64.b64encode(my_stringIObytes_1.read()).decode("ascii")

    plt.imshow(pred_image_2,cmap="gray")
    plt.axis("off")
    my_stringIObytes_2 = io.BytesIO()
    plt.savefig(my_stringIObytes_2, format='png',bbox_inches="tight")
    my_stringIObytes_2.seek(0)
    pred_image_b64_2 = base64.b64encode(my_stringIObytes_2.read()).decode("ascii")

    # Dump image to storage
    # with open("image.png", "wb") as f:
    #     f.write(b.read())

    return pred_image_b64_1,pred_image_b64_2,pred_image_1,pred_image_2

def get_mask(mask_file):

    # Preprocessing the input image
    mask = cv.imdecode(np.fromstring(mask_file.read(), np.uint8), cv.IMREAD_GRAYSCALE)
    # downsample the input image to 512 x 512 x 3
    mask = cv.resize(mask, (512,512))

    mask = mask.astype(np.uint8)

    return mask

if __name__ == "__main__":
    app.run(debug=True)
