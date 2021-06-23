import os
import argparse
import json
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import requests
import cv2 as cv
from skimage import img_as_float32
import matplotlib.pyplot as plt
# from keras.applications import inception_v3
# from keras.preprocessing import image

# Argument parser for giving input image_path from command line
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path of the image")
args = vars(ap.parse_args())

image_path = args['image']
# Preprocessing our input image
image = img_as_float32(cv.imread(image_path, cv.IMREAD_COLOR))

# downsample the input image to 512 x 512 x 3
image = cv.resize(image, (512,512))

payload = {
    "instances": [{'input_image': image.tolist()}]
}

# sending post request to TensorFlow Serving server
# r = requests.post('http://localhost:9000/v1/models/Segmentation:predict', json=payload)
r = requests.post('http://localhost:9002/v1/models/Segmentation2:predict', json=payload)
pred = json.loads(r.content.decode('utf-8'))

temp = np.array(pred['predictions'])
# print('Prediction shape: ',temp.shape)
pred_image = np.squeeze(temp[0]>0.5)
pred_image = pred_image.astype(np.uint8)
# print(pred_image)
display = np.invert(pred_image)
plt.imshow(display,cmap='binary')
plt.show()
# print('Prediction shape: ',pred_image.shape)
# print(pred_image.dtype)

status = cv.imwrite(f'{os.getcwd()}/pred_image.jpg',pred_image)
print("Image written to file-system : ",status)

# Decoding the response
# decode_predictions(preds, top=5) by default gives top 5 results
# You can pass "top=10" to get top 10 predicitons
# print(json.dumps(inception_v3.decode_predictions(np.array(pred['predictions']))[0]))