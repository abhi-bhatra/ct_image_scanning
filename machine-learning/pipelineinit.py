import time
import kfp
from kflow_model import *
import subprocess
import threading


def run_ml_pipeline():
    subprocess.run(["kubectl", "port-forward", "-n",
                   "kubeflow", "svc/ml-pipeline-ui", "8080:80"])

def run_ml_wf():
    client = kfp.Client(host='http://localhost:8080/')

    client.create_run_from_pipeline_func(
        my_pipeline,
        arguments={
            'url': 'https://rancherdataset.blob.core.windows.net/dataset/archive.tar.gz'
        })

while 1:
    # Code goes Here
    a = threading.Thread(target=run_ml_pipeline)
    b = threading.Thread(target=run_ml_wf)
    a.start()
    b.start()
    break
