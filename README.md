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
