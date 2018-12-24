import pickle
import gzip
from images import folder_resize, convert_images
from keras.models import load_model
import os
import pandas as pd
import numpy as np
from PIL import Image
from images import save_obj, load_obj, convert_images

# Path to original photos
folder_path = "/home/justina/Desktop/instagrammability/selfies/original"
model_path = "./models/weights.50-0.21.hdf5"
model = load_model(model_path)

X_test =load_obj("./models/obj/X_test_resnet50")
y_test = load_obj("./models/obj/y_test_resnet50")
data = "./images/training/data/quantile_ninety.csv"
IMAGE_DIR = "./images/training/resized"

images = pd.read_csv(data, usecols=['filename', 'norm_score', 'museum'])
paths = []
for filename, museum in zip(images.filename.tolist(), images.museum.tolist()):
    paths.append(os.path.join(IMAGE_DIR, museum, filename))
# filenames = folder_resize(folder_path)
# head, tail = os.path.split(folder_path)
X_total = convert_images(paths, 3, 224, 224, "resnet50")
# # numpy array

test_set = []
for img, path in zip(X_total, paths):
    for i, image in enumerate(X_test):
        if np.array_equal(image, img):
            prediction = model.predict(np.expand_dims(image, axis=0))[0][0]
            true = y_test[i]
            mse = (true - prediction)**2

            test_set.append((path, prediction, true, mse))
test_set_sorted = sorted(test_set, key=lambda x: x[1], reverse = True)

for i, (path, prediction, true, mse) in enumerate(test_set_sorted):
    im = Image.open(path)
    head, tail = os.path.split(path)
    im.save("/home/justina/Desktop/instagrammability/data/training/101_test/{}_{}".format(i, tail))

labels = ['Path', 'Prediction', 'True', 'MSE']
df = pd.DataFrame.from_records(test_set_sorted, columns=labels)

print("Number of images: {}".format(len(test_set)))
df.to_csv('/home/justina/Desktop/instagrammability/data/training/101_test/100_test.csv')

# print(test_set)
