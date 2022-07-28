# Cancer Prediction using CT Medical Images
![dataset-cover](https://user-images.githubusercontent.com/63901956/175071624-96dabb0b-912e-4ff1-bf6b-bc0202c6ec11.jpg)

https://www.kaggle.com/datasets/kmader/siim-medical-images

### Overview

**Dataset**

The dataset is designed to allow for different methods to be tested for examining the trends in CT image data associated with using contrast and patient age. The basic idea is to identify image textures, statistical patterns and features correlating strongly with these traits and possibly build simple tools for automatically classifying these images when they have been misclassified (or finding outliers which could be suspicious cases, bad measurements, or poorly calibrated machines)

**Model**

It is a Machine Learning Model trained on Keras, on top of Tensorflow. Complete reference to the notebook can be found here: [Jupyter Notebook](https://github.com/abhi-bhatra/ct_image_scanning/blob/master/cancer_detection.ipynb)

### Walkthrough

To start working with this model, we will follow these steps:

1. Clone the repo `git clone https://github.com/abhi-bhatra/ct_image_scanning.git`
2. Ensure to checkout on `master` branch: `git checkout master`
3. Install the requirements: `pip install -r ct_image_scanning/cancer_app/requirements.txt`
4. After the requirements are install, also ensure that **jupyter-notebook** is also installed: [Install Jupyter](https://jupyter.org/install)
5. Now, run the notebook, you can see the file named as **cancer_detection.ipynb**.
6. Open the Notebook and run the code step by step.
7. At the end you can see the **model_dicom_cancer.h5** is created. This is our trained Machine Learning Model.

**Till the above steps. we have successfully trained our Machine Learning Model**

Now, let's create a **Flask** application to perform prediction
File Structure is as follows:
1. `app.py`: This is the core of Flask application. All the Machine Learning Prediction codes resides in this Directory
2. 'Dockerfile': docker image of the Flask Application.
3. 'db.py': storing the images uploaded by the user
4. Use `flask run` to test the application in local at: `http://127.0.0.1:5000`

**Till the above steps. we have successfully run our Flask Application in Local**

Now, let's create a **kustomzie** manifest to run the application
File Structure is as follows:
1. `kustomization.yaml`: It contains the kubernetes manifests structure
2. `namespace.yaml`: It is the namespace created as Healthcare
3. `deployment.yaml`: This is the deployment manifest
4. `service.yaml`: This file will container the service
5. Run `kubectl apply -k k8s/` to apply and run the application in k8s clusters

This project is mentored by **Bryan Gartner, Ann Davis and Brian Fromme**. Dataset is taken from https://www.kaggle.com/
