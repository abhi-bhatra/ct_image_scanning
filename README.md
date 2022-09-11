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

3. **Interface #3**: Rancher dashboard to monitor the kubernetes cluster and resources deployed on it.

4. **Interface #4**: Kubeflow dashboard to visualize Kubeflow Pipelines.

![dataset-cover](https://user-images.githubusercontent.com/63901956/175071624-96dabb0b-912e-4ff1-bf6b-bc0202c6ec11.jpg)

### Technologies Used
1. **Python** (NumPy, Pandas, OpenCV) for Dataset and Images manipulation
2. **Convolutional Neural Net (CNN)** on CT Images with **Keras** on top of **Tensorflow**
3. **Flask** is used as a micro-web framework to design the backend.
4. **HTML/CSS/JS** for designing the interface.
5. **Docker** used to build containerized applications
6. **Kubernetes** used for complete software deployment and orchestrating the containers. Compatible with K3S/RKE/RKE2 distributions.
7. **Rancher** is used for Kubernetes Cluster management and various UI can be accessed with the help of Rancher.
8. **Kubeflow** is used to design ML pipelines to orchestrate workflow running on the Cluster 
9. **Longhorn** is a CSI, used as a storageclass and mounted as a volume within the pods to share the data and information locally.

### Application Structure

Application comprises of following document:

- application
- dataset
- documentation
- kubernetes-manifests
- machine-learning


#### Dataset
The dataset is imported from Kaggle, you can check out the dataset at [ official kaggle site ](https://www.kaggle.com/datasets/kmader/siim-medical-images). It is designed to allow for different methods to be tested for examining the trends in CT image data associated with using contrast and patient age. The basic idea is to identify image textures, statistical patterns and features correlating strongly with these traits and possibly build simple tools for automatically classifying these images when they have been misclassified (or finding outliers which could be suspicious cases, bad measurements, or poorly calibrated machines) 

#### Machine Learning
It is a Convolutional Neural Network Machine Learning Model trained on Keras, on top of Tensorflow. Complete reference to the notebook can be [ found on this Jupyter Notebook](https://github.com/abhi-bhatra/ct_image_scanning/blob/master/cancer_detection.ipynb)

#### Kubernetes Manifests
The Kubernetes Manifests are used to deploy the application on the cluster. The manifests are divided into followin parts:   

- dataset: dataset manifests are used to deploy the volumes on the cluster and claim those persistent volumes to the pods.

- doctor-app: these manifests are used to deploy the doctor dashboard application on the cluster.

- lab-technician-app: these manifests are used to deploy the lab technician application on the cluster.

- kubeflow: these manifests are used to deploy the kubeflow pipelines on the cluster.

#### Documentation
It consist of ASCII Doc files which are used to generate the documentation for the project. The documentation is generated using [ OpenSUSE Daps ](https://en.opensuse.org/openSUSE:Daps) tool.

#### Application
It consist of the application code for the project. The application is divided into two parts:

- Lab-tech
- Doctor-app

**Lab Technician Interface**: Lab Technician Interface is responsible for getting DICOM image as input. The person (Radiologits, Lab Technician, Physicians) could alter the information such as Contrast, Brightness and Angle of rotation of the DICOM image. They can also read all the information associated with the DICOM image (Modality: CT Scan).

**Doctor Dashboard Interface**: Doctor Dashboard is designed for the doctors to examine the report send by the Lab Technician. It receives the report of a patient and displays it to the user, predicting whether or not person is suffering from cacner. If doctor will not be satisfied with the response, they can send the image for the retraining with the correct label attached to it.

### Run the Application

To start working with this model, we will follow these steps:

**Note: Kubernetes Cluster should be deployed as a prerequisite task**

1. Clone the repo 
`git clone https://github.com/abhi-bhatra/ct_image_scanning.git`
2. Ensure to checkout on **master** branch: 
`git checkout UI_base`
3. Set-Up Application on k8s cluster:
    ```shell
    cd kubernetes-manifests/
    kubectl apply -f namespace.yaml

    kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.3.1/deploy/longhorn.yaml
    kubectl patch storageclass longhorn -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

    cd dataset/ && kubectl apply -k . && cd ..
    
    cd lab-tech/ && kubectl apply -k . && cd ..

    cd doctor-app && kubectl apply -k . && cd ..
    
    cd kubeflow/ && bash kflowsetup.sh
    ```
    
4. Check if all the resources are installed correctly:
`kubectl get all -n cancerns`


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

