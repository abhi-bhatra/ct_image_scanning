import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from flask import Flask, request, render_template, send_from_directory, flash
from msrest.authentication import ApiKeyCredentials
from dotenv import load_dotenv
from skimage.transform import resize

load_dotenv()
app = Flask(__name__)

app.secret_key = "secret key"
UPLOAD_FOLDER = '../dst/uploads/'
DOWNLOAD_FOLDER = '../dst/downloads/'
ALLOWED_EXTENSIONS = set(['dcm'])

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

# def predict(image_path):
#     model_h5 = tf.keras.models.load_model(
#         './model_dicom_cancer.h5', custom_objects={'KerasLayer': hub.KerasLayer})

#     pred90 = model_h5.predict(image_path.reshape(1, 256, 256, 1))
#     pred90 = pred90[0][1]*100
#     if int(pred90) < 90:
#         val = 'Normal'
#     else:
#         val = 'Cancer'
#     return val

# def read_dicom(ds):
#     parameters=[]
#     for i in ds:
#         parameters.append(str(i))
#     new_para=[]
#     for i in parameters:
#         new_para.append(i[13:])
#     dict_item = {re.sub(' +', ' ', i[:35]):re.sub(' +', ' ', i[36:]) for i in new_para}
#     return dict_item

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def get_gallery():
    image_names = os.listdir(app.config['DOWNLOAD_FOLDER'])
    new_names=[]
    for i in image_names:
        i=i.split('.')[0]
        new_names.append(i)
    return render_template("gallery.html", image_names=new_names)

@app.route('/<path:filename>')
def send_image(filename):
    new_filename=filename+'.jpg'
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], new_filename)

@app.route('/upload/<path:filename>')
def upload_image(filename):
    new_filename=filename+'.jpg'
    return render_template("upload.html", image_name=new_filename)

@app.route('/predict/<string:id>', methods=['GET','POST'])
def predict(id):
    # filename = id
    # image_names = os.listdir(app.config['UPLOAD_FOLDER']) 
    # image_path=''
    # for i in image_names:
    #     if i.split('.')[0]==filename:
    #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], i)
    #         break
    # ds = dicom.dcmread(image_path)
    # test90 = ds.pixel_array
    # IMG_PX_SIZE = 256
    # resized90 = resize(test90, (IMG_PX_SIZE, IMG_PX_SIZE, 1), anti_aliasing=True)

    ct_image = ''
    with open(os.path.join(app.config['DOWNLOAD_FOLDER'], id+'.jpg'), 'rb') as image_contents:
        results = predictor.classify_image(
            project_id, publish_iteration_name, image_contents.read())
        for prediction in results.predictions:
            if prediction.probability * 100 > 95:
                # if prediction.tag_name == "chest":
                #     ct_image = predict(resized90)
                #     ct_image = ''.join(ct_image)
                #     metadata = read_dicom(ds)
                # else:
                ans = prediction.tag_name
                ct_image = ''.join(ans)
                break
            else:
                ct_image = ''.join("We can only predict Cancer present in Chest images")
    flash('Image successfully uploaded and displayed below')
    return render_template('predict.html', id=id, ct_image=ct_image)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
