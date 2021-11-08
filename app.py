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
solution = ""

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
        
    return render_template('result.html',nameimg = nameimg,prob = prob, result=result, solution=solution)
#End of main

def classify():
    global pathimg, nameimg, prob, result, solution
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
    solution = solutions(result)


Bacteria = """
A plant with bacterial spot cannot be cured.
Remove symptomatic plants from the field or greenhouse to prevent the spread of bacteria to healthy plants.
Burn, bury or hot compost the affected plants and DO NOT eat symptomatic fruit.
Using pathogen-free seed and disease-free transplants, when possible, is the best way to avoid bacterial spot on tomato.
Avoiding sprinkler irrigation and cull piles near greenhouse or field operations, and rotating with a nonhost crop also helps control the disease.

You can use following Fertilizers: Bonide Citrus, Fruit & Nut Orchard Spray (32 Oz), Monterey Neem Oil
"""
Fungi = """
If it ocuurs in rainy season, it is Early Blight, then you may need to:
Rotate Your Crops, Purge Nightshades and Volunteer Tomato Plants, Keep Your Plants Dry, Stake Your Plants, Remove Infected Plants.
As for the treatment, you can use Copper Fungicide Dust. Use either diluted as a spray, or dust the powder onto the foliage, every three days.
If you see the black spots, it is likely that your tomato plants are infected with Septoria.
Mix of copper and sulfur that has been used to control fungi since the 1800s.
"""
Healthy = """
As your tomato plant is Healthy, you can use simple management practices that are usually sufficient to hold back full-blown infections in tomato plants and keep them healthy enough to produce a good crop.
Tomato plants have surprisingly low water needs and overwatering can promote disease.
Don't shower your tomatoes with sprinkler as it leads to fungal diseases, instead use drip irrigation.
Water in the Morning.
Remove Infected Leaves Immediately.
Tomatoes are heavy feeders and will have greater disease resistance with a few boosts of fertilizer during the growing season. Once the fruit has set, apply a high phosphorus fertilizer every three weeks.
"""
Mite = """
Prune leaves, stems and other infested parts of plants well past any webbing and discard in trash (and not in compost piles).
Don’t be hesitant to pull entire plants to prevent the mites spreading to its neighbors.
Use the Bug Blaster to wash plants with a strong stream of water and reduce pest numbers.
Commercially available beneficial insects, such as ladybugs, lacewing and predatory mites are important natural enemies. For best results, make releases when pest levels are low to medium.
Dust on leaves, branches and fruit encourages mites. A mid-season hosing (or two!) to remove dust from trees is a worthwhile preventative.
Insecticidal soap or botanical insecticides can be used to spot treat heavily infested areas.
"""
Mold = """
Plant resistant cultivars when available.
Remove volunteers from the garden prior to planting and space plants far enough apart to allow for plenty of air circulation.
Water in the early morning hours, or use soaker hoses, to give plants time to dry out during the day — avoid overhead irrigation.
Destroy all tomato and potato debris after harvest.
As you can use following Fungicides : 
1. Difenoconazole and Cyprodinil
2. Difenoconazole and Mandipropamid
3. Cymoxanil and Famoxadone
4. Azoxystrobin and Difenoconazole
"""
Virus = """
The leaves are mottled with yellow, white, and light and dark green spots, which appear to be elevated.
Fungicides will not treat this viral disease.
Avoid working in the garden during damp conditions (viruses are easily spread when plants are wet).
Frequently wash your hands and disinfect garden tools, stakes, ties, pots, greenhouse benches, etc. 
Remove and destroy all infected plants.Do not compost.
Do not save seed from infected crops.

As Leaves often appear to be thick and leathery and becomes usually becomes yellow:
Use a neonicotinoid insecticide, such as dinotefuran (Venom) imidacloprid (AdmirePro, Alias, Nuprid, Widow, and others) or thiamethoxam (Platinum), as a soil application or through the drip irrigation system at transplanting of tomatoes or peppers. 
Cover plants with floating row covers of fine mesh (Agryl or Agribon) to protect from whitefly infestations.
Practice good weed management in and around fields to the extent feasible.
Remove and destroy old crop residue and volunteers on a regional basis.
"""


def solutions(result):
    switcher = {
        "Bacteria": Bacteria,
        "Fungi": Fungi,
        "Healthy":Healthy,
        "Mite":Mite,
        "Mold":Mold,
        "Virus":Virus
    }
    return switcher.get(result,"Disease not found")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
