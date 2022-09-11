import kfp
import kfp.components as comp

# Download the Data
web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml')

# Preprocess the CSV
def preprocess_csv(file_path: comp.InputPath('Tarball'),
                   output_csv: comp.OutputPath('CSV')):
    import os
    import pandas as pd
    import tarfile
    import os
    from glob import glob
    import numpy as np
    from skimage.io import imread
    import re

    tarfile.open(name=file_path, mode="r|gz").extractall('data')
    PATH = 'data/archive/'
    df = pd.read_csv(os.path.join(PATH, "overview.csv"), index_col=0)
    df['Contrast'] = df['Contrast'].map(lambda x: 1 if x else 0)

    all_images_list = glob(os.path.join(PATH, 'tiff_images', '*.tif'))
    np.expand_dims(imread(all_images_list[0])[::4, ::4], 0).shape
    def jimread(x): return np.expand_dims(imread(x)[::2, ::2], 0)
    check_contrast = re.compile(
        r'/tiff_images/ID_([\d]+)_AGE_[\d]+_CONTRAST_([\d]+)_CT.tif')
    label = []
    id_list = []
    for image in all_images_list:
        id_list.append(check_contrast.findall(image)[0][0])
        label.append(check_contrast.findall(image)[0][1])

    label_list = pd.DataFrame(label, id_list)
    images = np.stack([jimread(i) for i in all_images_list], 0)

    df.to_csv(output_csv, index=False, header=False)


# Train the Model
def train_model(file_path: comp.InputPath('Tarball'), file_csv: comp.InputPath('CSV'), model_path: comp.OutputPath('TFModel')):
    import os
    import pandas as pd
    import tarfile
    import os
    from glob import glob
    from skimage.io import imread
    import re
    from sklearn.model_selection import train_test_split
    import numpy as np
    import keras
    from keras.models import Sequential
    from keras.layers import Dense, Flatten
    from keras.optimizers import Adam
    from keras.layers import Conv2D, MaxPooling2D
    from pathlib import Path

    BASE_IMG = file_csv
    tarfile.open(name=file_path, mode="r|gz").extractall('data')
    PATH = 'data/archive/'
    df = pd.read_csv(os.path.join(PATH, "overview.csv"), index_col=0)
    df['Contrast'] = df['Contrast'].map(lambda x: 1 if x else 0)

    all_images_list = glob(os.path.join(PATH, 'tiff_images', '*.tif'))
    np.expand_dims(imread(all_images_list[0])[::4, ::4], 0).shape
    def jimread(x): return np.expand_dims(imread(x)[::2, ::2], 0)
    check_contrast = re.compile(
        r'/tiff_images/ID_([\d]+)_AGE_[\d]+_CONTRAST_([\d]+)_CT.tif')

    label = []
    id_list = []
    for image in all_images_list:
        id_list.append(check_contrast.findall(image)[0][0])
        label.append(check_contrast.findall(image)[0][1])

    label_list = pd.DataFrame(label, id_list)
    images = np.stack([jimread(i) for i in all_images_list], 0)

    batch_size = 20
    epochs = 5

    X_train, X_test, y_train, y_test = train_test_split(
        images, label_list, test_size=0.1, random_state=0)
    n_train, depth, width, height = X_train.shape
    n_test, _, _, _ = X_test.shape
    input_shape = (width, height, depth)

    input_train = X_train.reshape((n_train, width, height, depth))
    input_train.astype('float32')
    input_train = input_train / np.max(input_train)

    input_test = X_test.reshape(n_test, *input_shape)
    input_test.astype('float32')
    input_test = input_test / np.max(input_test)

    output_train = keras.utils.to_categorical(y_train, 2)
    output_test = keras.utils.to_categorical(y_test, 2)

    model2 = Sequential()
    model2.add(Conv2D(50, (5, 5), activation='relu', input_shape=input_shape))
    model2.add(MaxPooling2D(pool_size=(3, 3)))
    model2.add(Conv2D(30, (4, 4), activation='relu', input_shape=input_shape))
    model2.add(MaxPooling2D(pool_size=(2, 2)))
    model2.add(Flatten())
    model2.add(Dense(2, activation='softmax'))

    model2.compile(loss='categorical_crossentropy',
                   optimizer=Adam(),
                   metrics=['accuracy'])

    model2.fit(input_train, output_train,
               batch_size=batch_size,
               epochs=epochs,
               verbose=1,
               validation_data=(input_test, output_test))

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    model2.save(model_path)


# Predict with the Model
def predict_model(file_path: comp.InputPath('Tarball'), model_path: comp.InputPath('TFModel')):
    import os
    import pandas as pd
    import tarfile
    from glob import glob
    import numpy as np
    from skimage.io import imread
    import re
    from sklearn.model_selection import train_test_split
    import keras
    from tensorflow import keras

    model = keras.models.load_model(model_path)
    tarfile.open(name=file_path, mode="r|gz").extractall('data')
    PATH = 'data/archive/'

    all_images_list = glob(os.path.join(PATH, 'tiff_images', '*.tif'))
    np.expand_dims(imread(all_images_list[0])[::4, ::4], 0).shape
    def jimread(x): return np.expand_dims(imread(x)[::2, ::2], 0)
    check_contrast = re.compile(
        r'/tiff_images/ID_([\d]+)_AGE_[\d]+_CONTRAST_([\d]+)_CT.tif')
    label = []
    id_list = []
    for image in all_images_list:
        id_list.append(check_contrast.findall(image)[0][0])
        label.append(check_contrast.findall(image)[0][1])
    label_list = pd.DataFrame(label, id_list)
    images = np.stack([jimread(i) for i in all_images_list], 0)

    X_train, X_test, y_train, y_test = train_test_split(
        images, label_list, test_size=0.1, random_state=0)
    n_train, depth, width, height = X_train.shape
    n_test, _, _, _ = X_test.shape
    input_shape = (width, height, depth)

    input_test = X_test.reshape(n_test, *input_shape)
    input_test.astype('float32')
    input_test = input_test / np.max(input_test)

    print(model.predict(input_test))


create_step_merge_csv = kfp.components.create_component_from_func(
    func=preprocess_csv,
    output_component_file='component1.yaml',
    base_image='python:3.7',
    packages_to_install=['pandas', 'scikit-image', 'numpy', 'glob2'])

create_step_train_model = kfp.components.create_component_from_func(
    func=train_model,
    output_component_file='component2.yaml',
    base_image='python:3.7',
    packages_to_install=['pandas', 'numpy', 'tensorflow', 'scikit-learn', 'scikit-image', 'keras', 'glob2'])

create_predict_model = kfp.components.create_component_from_func(
    func=predict_model,
    output_component_file='component3.yaml',
    base_image='python:3.7',
    packages_to_install=['pandas', 'numpy', 'tensorflow', 'scikit-learn', 'scikit-image', 'keras', 'glob2'])


def my_pipeline(url):
    web_downloader_task = web_downloader_op(url=url)
    merge_csv_task = create_step_merge_csv(
        file=web_downloader_task.outputs['data'])
    train_model_task = create_step_train_model(
        file=web_downloader_task.outputs['data'], file_csv=merge_csv_task.outputs['output_csv'])
    predict_model_task = create_predict_model(
        file=web_downloader_task.outputs['data'], model=train_model_task.output)

