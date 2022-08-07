import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pydicom as dicom
from skimage.transform import resize
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import cv2
import numpy as np
import re

load_dotenv()

app = Flask(__name__)

app.secret_key = "secret key"
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['dcm'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 512 * 512
PNG = False

ENDPOINT = os.environ['ENDPOINT']
prediction_key = os.environ['PREDICTION_KEY']
project_id = os.environ['PROJECT_ID']

prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

publish_iteration_name = "Iteration3" # Change the Iteration Value

def read_dicom(ds):
    parameters=[]
    for i in ds:
        parameters.append(str(i))
    new_para=[]
    for i in parameters:
        new_para.append(i[13:])
    dict_item = {re.sub(' +', ' ', i[:35]):re.sub(' +', ' ', i[36:]) for i in new_para}
    return dict_item

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def BrightnessContrast(brightness=0):
    brightness = cv2.getTrackbarPos('Brightness', 'MyImage')
    contrast = cv2.getTrackbarPos('Contrast', 'MyImage')
    effect = controller(img_adjust, brightness, contrast)
    cv2.imshow('Effect', effect)

def controller(img, brightness=255, contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255
        else:
            shadow = 0
            max = 255 + brightness
        al_pha = (max - shadow) / 255
        ga_mma = shadow
        cal = cv2.addWeighted(img, al_pha, img, 0, ga_mma)
    else:
        cal = img
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
        cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)
    cv2.putText(cal, 'B:{},C:{}'.format(brightness, contrast), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return cal

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    ct_image = ''
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url=app.config['UPLOAD_FOLDER']+filename
        ds = dicom.dcmread(file_url)
        test90 = ds.pixel_array
        test90 = ds.pixel_array.astype(float)
        threshold = 500
        test90 = (np.maximum(test90, 0) / (np.amax(test90) + threshold)) * 255.0
        if PNG == False:
            filename = filename.replace('.dcm', '.jpg')
        else:
            filename = filename.replace('.dcm', '.png')
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), test90)
        
        # Test on Adjusting Image
        file_url=app.config['UPLOAD_FOLDER']+filename
        img_adjust = cv2.imread(file_url)
        cv2.namedWindow('MyImage')
        cv2.imshow('MyImage', img_adjust)
        cv2.createTrackbar('Brightness', 'MyImage',255, 2 * 255, BrightnessContrast)
        cv2.createTrackbar('Contrast', 'MyImage',255, 2 * 255, BrightnessContrast)
        BrightnessContrast(0)
        cv2.waitKey(0)


        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as image_contents:
            results=predictor.classify_image(project_id, publish_iteration_name, image_contents.read())
            for prediction in results.predictions:
                if prediction.probability * 100 > 95:
                    ans = prediction.tag_name
                    ct_image = ''.join(ans)
                    break
            
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename, ct_image=ct_image)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0')