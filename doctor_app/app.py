import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from flask import Flask, request, render_template, send_from_directory
from msrest.authentication import ApiKeyCredentials
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='../dst')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['dcm','jpg','jpeg','png'])

ENDPOINT = os.environ['ENDPOINT']
prediction_key = os.environ['PREDICTION_KEY']
project_id = os.environ['PROJECT_ID']

prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
publish_iteration_name = "Iteration3" # Change the Iteration Value


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/<path:filename>')
def send_image(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/")
def get_gallery():
    image_names = os.listdir(app.static_folder)
    print(image_names)
    return render_template("gallery.html", image_names=image_names)

@app.route('/predict/<string:id>',methods=['GET','POST'])
def predict(id):
    ct_image=''
    with open(os.path.join(app.static_folder, id), 'rb') as image_contents:
        results=predictor.classify_image(project_id, publish_iteration_name, image_contents.read())
        for prediction in results.predictions:
            if prediction.probability * 100 > 95:
                ans = prediction.tag_name
                ct_image = ''.join(ans)
                break
    # print(id)
    return render_template('predict.html',id=id, ct_image=ct_image)

if __name__ == "__main__":
    app.run(port=5002, debug=True)