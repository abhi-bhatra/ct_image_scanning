import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
import tensorflow_hub as hub
import pydicom as dicom
from skimage.transform import resize
import cv2
import PIL

app = Flask(__name__)

app.secret_key = "secret key"
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['dcm'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 512 * 512

PNG = False

def predict(image_path):
    model_h5 = tf.keras.models.load_model(
    './model_dicom_cancer.h5', custom_objects={'KerasLayer': hub.KerasLayer})

    pred90 = model_h5.predict(image_path.reshape(1,256, 256, 1))
    pred90 = pred90[0][1]*100
    if int(pred90) < 90:
        val='Normal'
    else:
        val='Cancer'
    return val

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    ct_image=''
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url=app.config['UPLOAD_FOLDER']+filename
        ds = dicom.dcmread(file_url)
        test90 = ds.pixel_array
        IMG_PX_SIZE = 256
        resized90 = resize(test90, (IMG_PX_SIZE, IMG_PX_SIZE, 1), anti_aliasing=True)
        ct_image=predict(resized90)
        ct_image=''.join(ct_image)
        if PNG == False:
            filename = filename.replace('.dcm', '.jpg')
        else:
            filename = filename.replace('.dcm', '.png')
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), test90)
        # plt.imshow(test90)
        # plt.savefig('static/uploads/'+str(filename))
        # path_img = 'static/uploads/'+str(filename)
        
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename, ct_image=ct_image)
    else:
        flash('Allowed image types are -> dcm')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()