from flask import Flask, request, render_template
import os
import cv2
import numpy as np
import os.path as path
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model



app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
nameimg=""
pathimg=""
prob = 0
result = ""



@app.route('/')
def index():
    return render_template("main.html")
#End of / [index]

@app.route('/main', methods=["POST"])
def main():
    global nameimg, pathimg
    uploads = path.join(APP_ROOT, 'static\\')
    print(uploads)

    if not path.isdir(uploads):
        os.mkdir(uploads)
    for img in os.listdir(uploads):
        pathimg = uploads + img
        os.remove(pathimg)
        print(pathimg+" removed.")

    for file in request.files.getlist("file"):
        nameimg = 'tomatoleaf.JPG'
        pathimg = "/".join([uploads,nameimg])
        print(pathimg)
        file.save(pathimg)
    try:
        classify()

    except Exception as e:
        print(e)
        

    return render_template('result.html',nameimg = nameimg,prob = prob, result=result)
#End of main

def classify():
    global pathimg, nameimg, prob, result
    sizeimg = (256,256)
    modelpath = "model2resnet.h5"
    image = cv2.imread(pathimg)
    try:
        image = cv2.resize(image, sizeimg)
        image = image.astype("float")
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
    except Exception as e:
        print(e)

    model = load_model(modelpath)
    pred = model.predict(image)[0] 
    pred1 = np.argmax(pred)
    classes = ['Bacteria', 'Fungi', 'Healthy', 'Mite', 'Mold', 'Virus']
    result = classes[pred1]
    prob = max(pred) * 100
    print(prob)
    prob = float("{0:.2f}".format(prob))
    print(result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
