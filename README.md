# OpenSUSE Rancher (Google Summer of Code)

Welcome to the openSUSE Rancher (GSoC) 👋! GSoC is a great program to get some experience with open source development. **OpenSUSE Rancher** aims to build analytical edge ecosystem workloads. This project is an end-to-end example approach in the Healthcare vertical.

### About Google Summer of Code
[Google Summer of Code<sup>TM</sup>](https://summerofcode.withgoogle.com/) is a summer program that offers stipends to develop software for open source projects. 

### Project Idea
OpenSUSE Project is a worldwide effort that promotes the use of Linux, tools around it, and open source. OpenSUSE Rancher is a cluster management tool and we are aimed to build an **Analytical Edge Ecosystem Worload**, you can know more about the project at [ Google Summer of Code portal ](https://summerofcode.withgoogle.com/programs/2022/projects/MNFtN4so).  If you have any questions about any of the ideas, please comment in the issues on GitHub or ask us on the [ chat ](https://chat.opensuse.org/) / [ Telegram ](https://en.opensuse.org/openSUSE:Telegram) / [ Mailing Lists ](https://lists.opensuse.org/archives/list/project@lists.opensuse.org/)

### About Cancer Prediction System

**Overview**
The Cancer Prediction system is a Machine Learning based resource designed to provide the broad information and the cancer status of the person from the CT Scanned Images. The application is built on top of cluster and is divided into two interfaces. 
1. **Interface #1**: Lab Technician Interface, used by the Lab Technician to manipulate the scanned DICOM images and send those images to Doctor's Dashboard (Interface #2)

2. **Interface #2**: Doctor Dashboard, used by the doctor to see the CT Scanned Images (or DICOM) Images and can see the predicted results, if doctor is not satisfied with the results, they can send the image for retraining.

![dataset-cover](https://user-images.githubusercontent.com/63901956/175071624-96dabb0b-912e-4ff1-bf6b-bc0202c6ec11.jpg)


**Dataset**
The dataset is imported from Kaggle, you can check out the dataset at [ official kaggle site ](https://www.kaggle.com/datasets/kmader/siim-medical-images). It is designed to allow for different methods to be tested for examining the trends in CT image data associated with using contrast and patient age. The basic idea is to identify image textures, statistical patterns and features correlating strongly with these traits and possibly build simple tools for automatically classifying these images when they have been misclassified (or finding outliers which could be suspicious cases, bad measurements, or poorly calibrated machines) 


**Machine Learning Model**
It is a Machine Learning Model trained on Keras, on top of Tensorflow. Complete reference to the notebook can be [ found on this Jupyter Notebook](https://github.com/abhi-bhatra/ct_image_scanning/blob/master/cancer_detection.ipynb)

**Technologies Used**
1. **Python** (NumPy, Pandas, OpenCV) for Dataset and Images manipulation
2. **Convolutional Neural Net (CNN)** on CT Images with **Keras** on top of **Tensorflow**
3. **Flask** is used as a micro-web framework to design the backend.
4. **HTML/CSS/JS** for designing the interface.
5. **Docker** used to build containerized applications
6. **Kubernetes** used for complete software deployment and orchestrating the containers. Compatible with K3S/RKE/RKE2 distributions.
7. **Rancher** is used for Kubernetes Cluster management and various UI can be accessed with the help of Rancher.
8. **Kubeflow** is used to design ML pipelines to orchestrate workflow running on the Cluster 
9. **Longhorn** is a CSI, used as a storageclass and mounted as a volume within the pods to share the data and information locally.

### Access the Application

To start working with this model, we will follow these steps:

1. Clone the repo `git clone https://github.com/abhi-bhatra/ct_image_scanning.git`
2. Ensure to checkout on `UI_base` branch: `git checkout UI_base`
3. Set-Up Application on k8s cluster:
    ```shell
    cd k8s/
    kubectl apply -f namespace.yaml
    cd dataset/ && kubectl apply -k dataset/ && cd ..
    kubectl apply -k lab-tech/
    kubectl apply -k doctor-app/
    cd kubeflow/ && bash kflowsetup.sh
    kubectl apply -f kubeflow-istio.yaml
    ```
    Check if all the resources are installed correctly: **`kubectl get all -n cancerns`**
4. **Flask** file Structure is as follows (Same is being followed for both the interfaces (Doctor's Dashboard and Lab Technician App)):
    4.1. `app.py`: This is the core of Flask application. All the Machine Learning Prediction codes resides in this Directory
    4.2. `Dockerfile`: docker image of the Flask Application.
    4.3. `templates/`: Store the frontend of Interface
    4.4. `<MODEL_NAME>.h5`: Our trained ML model
    4.5. `requirements.txt`: All the application dependency
4. Run the Flask application locally:
```shell
****Lab Technician App****
cd lab-tech/
python -m pip install requirements.txt
export DEBUG=1
flask run -p 5001

# Access at: http://localhost:5001/

****Doctor Dashboard****
cd doctor-app/
python -m pip install requirements.txt
export DEBUG=1
flask run -p 5002

# Access at: http://localhost:5002/
```

**Kubernetes Manifests**

Now, let's create a **kustomzie** manifest to run the application
File Structure is as follows:

1. `namespace.yaml`: It is the namespace created as Healthcare
2. `kustomization.yaml`: It contains the kubernetes manifests structure
    2.1. `deployment.yaml`: This is the deployment manifest
    2.2. `service.yaml`: This file will container the service
3. `Dataset/`: Dataset manifest contains the Kubernetes Job (to download the dataset), PVC (to mount the dataset as a volume)
4. `Rancher/`: Rancher manifest contains the Rancher resources (Rancher Cluster, Rancher Project, Rancher Namespace, Rancher Secret)
5. `lab-tech/`: Lab Technician manifest contains the Kubernetes Deployment, Service, PVC, Secret
6. `doctor-app/`: Doctor Dashboard manifest contains the Kubernetes Deployment, Service, PVC, Secret

### License
1. [http://creativecommons.org/licenses/by/3.0/](https://creativecommons.org/licenses/by/3.0/)
2. After the publication embargo period ends these collections are freely available to browse, download, and use for commercial, scientific and educational purposes as outlined in the Creative Commons Attribution 3.0 Unported License. Questions may be directed to help@cancerimagingarchive.net. Please be sure to acknowledge both this data set and TCIA in publications by including the following citations in your work:
3. **Data Citation**
`Albertina, B., Watson, M., Holback, C., Jarosz, R., Kirk, S., Lee, Y., … Lemmerman, J. (2016). Radiology Data from The Cancer Genome Atlas Lung Adenocarcinoma [TCGA-LUAD] collection. The Cancer Imaging Archive. http://doi.org/10.7937/K9/TCIA.2016.JGNIHEP5`
4. **TCIA Citation**
`Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. (paper)`


### Special Thanks
This project is mentored by **Bryan Gartner, Ann Davis, Brian Fromme and OpenSUSE Community**❤️. Really thankful to them for their guidance and support. 

### Demo Video

https://user-images.githubusercontent.com/63901956/189155172-33a03e87-de72-4d32-84cd-4d94df48ce20.mp4

