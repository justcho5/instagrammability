from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50
from keras.layers import Input, Flatten, Dense
from keras.models import Model
from keras import optimizers
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from keras.wrappers.scikit_learn import KerasRegressor
import pandas as pd
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping

import numpy as np
import sys
from images import save_obj, convert_images

def resnet50():
    """Returns a compiled ResNet50 model pretrained on ImageNet images"""

    # Get back the convolutional part of a VGG network trained on ImageNet
    model_resnet50_conv = ResNet50(weights='imagenet', include_top=False)
    # model_resnet50_conv.summary()

    # Create your own input format
    input = Input(shape=(224, 224, 3), name='image_input')

    # Use the generated model
    output_resnet50_conv = model_resnet50_conv(input)

    # Add the fully-connected layers
    x = Flatten(name='flatten')(output_resnet50_conv)
    x = Dense(1, activation='sigmoid', name='predictions')(x)

    # Create your own model
    model = Model(input=input, output=x)

    # In the summary, weights and layers from VGG part will be hidden, but they will be fit during the training
    # model.summary()
    for layer in model.layers:
        layer.trainable = False
    # Then training with your data !
    model.compile(loss="mean_squared_error",
                  optimizer=optimizers.Adam())
    return model


def vgg16():
    """Returns a compiled VGG16 model pretrained on ImageNet images"""

    # Get back the convolutional part of a VGG network trained on ImageNet
    model_vgg16_conv = VGG16(weights='imagenet', include_top=False)
    # model_vgg16_conv.summary()

    # Create your own input format (here 3x200x200)
    input = Input(shape=(224, 224, 3), name='image_input')

    # Use the generated model
    output_vgg16_conv = model_vgg16_conv(input)

    # Add the fully-connected layers
    x = Flatten(name='flatten')(output_vgg16_conv)
    x = Dense(50, activation='relu', name='fc1')(x)
    x = Dense(50, activation='relu', name='fc2')(x)
    x = Dense(1, activation='sigmoid', name='predictions')(x)

    # Create your own model
    model = Model(input=input, output=x)

    # In the summary, weights and layers from VGG part will be hidden, but they will be fit during the training
    # model.summary()
    for layer in model.layers:
        layer.trainable = False
    # Then training with your data !
    model.compile(loss="mean_squared_error", optimizer=optimizers.Adam())

    return model

models_to_str = {vgg16: 'vgg16',
                     resnet50: 'resnet50'}

str_to_models = {'vgg16': vgg16, 'resnet50':resnet50}

def predict(model, X_test):
    """Predict on fitted model.

    Args:
        model (keras training model): the trained model
        X_test (numpy array): unseen images as arrays

    Returns:
        Numpy array of predictions
        """

    return model.predict(X_test, batch_size=None, verbose=0, steps=None).flatten()

def cross_validation(model, x_tr, y_tr, batch = 32, epoch = 20, k = 3):
    
    X_train, X_test, y_train, y_test = train_test_split(x_tr, y_tr, test_size=100, random_state=33, shuffle = True)
    print("Train set size: {}, Test set size: {}".format(len(X_train), len(X_test)))

    # cross validation
    estimator = KerasRegressor(build_fn=model, epochs=epoch, batch_size=batch, verbose=True)
    print("{}-fold Cross Validation".format(k))
    # kfold = KFold(n_splits=splits, random_state=seed)
    # scores = cross_validate(estimator, x_tr, y_tr, cv=kfold, return_estimator=True, scoring='neg_mean_squared_error', n_jobs=4)
    scores = cross_val_score(estimator, X_train, y_train, groups=None, scoring='neg_mean_squared_error', cv=k, verbose=1, fit_params=None)
    mean_score = scores.mean()
    std_score = scores.std()
    print("Results: {}".format(scores))
    print("Results (avg): %.2f (%.2f) MSE" % (mean_score, std_score))

    return X_train, X_test, y_train, y_test

def fit_model(model_fn, X_train, y_train, X_test, y_test, batch = 32, epoch = 20):
    
    modelchkpt = ModelCheckpoint("./models/checkpoint_weights/weights.{epoch:02d}-{val_loss:.2f}.hdf5", monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=10, verbose=1, mode='auto', min_delta=0.0001, cooldown=0, min_lr=0.0001)
    hist = model_fn().fit(x=X_train, y=y_train, callbacks=[reduce_lr, modelchkpt], batch_size=batch, epochs=epoch, verbose=1, shuffle=True, validation_data = (X_test, y_test))
    save_obj(hist, "./models/obj/history_{}".format(models_to_str[model_fn]))
    save_obj(X_test, "./models/obj/X_test_{}".format(models_to_str[model_fn]))
    save_obj(y_test, "./models/obj/y_test_{}".format(models_to_str[model_fn]))

    return model_fn()

def train_and_save_model(inp):
    IMAGE_DIR = "./images/training/resized/"
    data = "./images/training/data/quantile_ninety.csv"

    np.seed = 1
    batch = 32
    epoch = 1
    splits = 2
    

    images = pd.read_csv(data, usecols=['filename', 'norm_score', 'museum'])[:200]
    paths = []
    for filename, museum in zip(images.filename.tolist(), images.museum.tolist()):
        paths.append("{}{}/{}".format(IMAGE_DIR, museum, filename))

    y_tr = images.norm_score.values

    if inp:
       models = inp
    else:
        models = ['resnet50']

    for mo in models:
        m=str_to_models[mo]
        model = m()
        print("{} Architecture".format(models_to_str[m]))
        x_tr = convert_images(paths, 3, 224, 224, models_to_str[m])
        # Splitting
        X_train, X_test, y_train, y_test = cross_validation(m, x_tr, y_tr, batch=batch, epoch = epoch, k=splits)
        model = fit_model(m, X_train, y_train, X_test, y_test, batch=batch, epoch = epoch)
        model.save('./models/{}_lastsave.h5'.format(models_to_str[m]))  # creates a HDF5 file 'my_model.h5'
    print('Done.')
    return X_test, y_test
