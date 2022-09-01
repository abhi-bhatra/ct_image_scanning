import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from flask import Flask, request, render_template, send_from_directory, flash
from msrest.authentication import ApiKeyCredentials
from dotenv import load_dotenv
from skimage.transform import resize
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import shutil
from PIL import Image 
import PIL

load_dotenv()
app = Flask(__name__)

app.secret_key = "secret key"
UPLOAD_FOLDER = '../ML_MODEL/dataset/train/'
DOWNLOAD_FOLDER = '../dst/downloads/'
ALLOWED_EXTENSIONS = set(['dcm', 'jpg'])

ENDPOINT = os.environ['ENDPOINT']
prediction_key = os.environ['PREDICTION_KEY']
project_id = os.environ['PROJECT_ID']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 512 * 512

prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
publish_iteration_name = "Iteration3"  # Change the Iteration Value

def predict_cancer(image_path):
    model_h5 = tf.keras.models.load_model(
        './image-model.h5', custom_objects={'KerasLayer': hub.KerasLayer})
    
    img = cv2.imread(os.path.join(app.config['DOWNLOAD_FOLDER'], image_path))
    img = cv2.resize(img, (512,512))
    img = img.reshape(1,512,512,3)
    pred90 = model_h5.predict(img)
    val = ''
    pred90 = pred90[0][0]*100
    if pred90 < 90.0:
        val = 'Normal'
    else:
        val = 'Cancer'
    return val

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def get_gallery():
    image_names = os.listdir(app.config['DOWNLOAD_FOLDER'])
    return render_template("gallery.html", image_names=image_names)

@app.route('/<path:filename>')
def send_image(filename):
    # filename=os.path.basename(filename)
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

@app.route('/predict/<path:id>')
def predict(id):
    ct_image=''
    status=''
    with open(os.path.join(app.config['DOWNLOAD_FOLDER'], id), 'rb') as image_contents:
        results=predictor.classify_image(project_id, publish_iteration_name, image_contents.read())
        for prediction in results.predictions:
            if prediction.probability * 100 > 95:
                if prediction.tag_name == "chest":
                    ct_image = predict_cancer(id)
                    ct_image = ''.join(ct_image)
                    return render_template('predict.html', id=id, ct_image=ct_image, status=None)
                else:
                    status = "Not a Chest Image"
                break
            else:
                status = "Not a Chest Image"
    return render_template('predict.html', id=id, ct_image=None, status=status)

@app.route('/retrain/<variable>', methods=['POST'])
def retrain(variable):
    # image_path = os.path.join(app.config['DOWNLOAD_FOLDER'], variable)
    if request.method == "POST":
        doc_name = request.form['name']
        # print(variable)
        status = request.form.get('cancer-detect')
        filename='test.jpg'   #os.path.basename(image_path)
        new_path=app.config['UPLOAD_FOLDER']+status+"/"
        shutil.move(os.path.join(app.config['DOWNLOAD_FOLDER'],variable), os.path.join(new_path,filename))
    return render_template('retrain.html', doc_name=doc_name)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
