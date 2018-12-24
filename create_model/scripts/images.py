# Scripts for image manipulation
from keras.preprocessing.image import img_to_array, load_img
import keras.applications.resnet50 as r
import keras.applications.vgg16 as v
from PIL import Image
from tqdm import tqdm
import os
from multiprocessing import Pool
import numpy as np
import pickle
import gzip


def save_obj(obj, name):
    """Save object

    Args:
        obj (any): object to be saved
        name (string): filename without extension

    """

    with gzip.open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """Load pickle object

    Args:
        name (string): filename without extension

    Returns:
        object of any type

    """
    with gzip.open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def crop(folder_path, file):
    """Crop image to dimensions 224 x 224

    Args:
        folder_path (str): pathname of directory where file lives
        file (str): filename with extension

    Returns:
        path where resized image is saved
    """
    im = Image.open(os.path.join(folder_path, file))
    width, height = im.size  # Get dimensions

    min_length = min(width, height);
    img_array = np.array(im)  # im2arr.shape: height x width x channel
    black_and_white = len(img_array.shape) == 2

    if black_and_white: # black and white
        new_img = np.zeros((224, 224))
        new_img = img_array[:min_length, :min_length]
    else:
        new_img = np.zeros((224, 224, 3))
        new_img = img_array[:min_length, :min_length, :]

    im = Image.fromarray(new_img)
    before = im.size
    im.thumbnail([224, 224], Image.ANTIALIAS)
    run = True
    path_tail = ""
    path_head = folder_path
    while run:
        head, tail = os.path.split(path_head)
        if tail == "original":
            new_path = os.path.join(head, "resized", path_tail, file)
            run = False
        else:
            path_tail = os.path.join(tail,path_tail)
            path_head = head

    im.save(new_path)
    w, h = im.size
    if w != 224 or h != 224:
        print("Before, After of {}: {}, {}".format(file, before, im.size))
    return new_path


def item_resize(x):
    """Resize image"""
    item, folder_path = x
    if item.endswith(".jpg") or item.endswith(".jpeg") or item.endswith(".png") or item.endswith(".JPG"):
        fullpath = os.path.join(folder_path, item)
        if os.path.isfile(fullpath):
            crop(folder_path, item)


def folder_resize(folder_path):
    """Resize images in a folder"""
    one_museum_files = os.listdir(folder_path)
    with Pool(10) as pool:
        lst = list(map(lambda item: (item, folder_path), one_museum_files))
        for each in tqdm(pool.imap(item_resize, lst), total=len(lst)):
            pass
    return one_museum_files


def print_size(path):
    """Print sizes of images in a folder"""
    folder = os.listdir(path)
    for item in folder:
        if item.endswith(".jpg"):
            im = Image.open(path + "/"+ item)
            print("Size", im.size, path + "/" + item)


def convert_images(image_filenames_lst, channels, height, width, model_name = 'resnet50'):
    """Convert images to arrays

        Args:
            image_filenames_lst (list): list of image paths
            channels (int): Number of image channels. RGB = 3, Greyscale = 1
            height (int): Final height of image in pixels
            width (int): Final width of image in pixels
            model_name (str): Either resnet50 or vgg16. Default is resnet50

        Returns:
            A numpy array with shape (Number of images, height, width, channels)

            """
    channels = channels
    image_height = height
    image_width = width

    x_tr = np.zeros((len(image_filenames_lst), image_height, image_width, channels))

    print("Converting images to array...")
    lst = list(enumerate(image_filenames_lst))
    for index, path in tqdm(lst, total=len(lst)):
        im = load_img(path, color_mode='rgb')
        img_array = img_to_array(im)
        x_tr[index] = img_array

    print("Done.")
    print("Number of data: {}".format(x_tr.shape))
    if model_name=='vgg16':
        x_tr = v.preprocess_input(x_tr)
    else:
        x_tr = r.preprocess_input(x_tr)
    return x_tr

def training_resize(datapath, original):
    all_museum_folders = os.path.join(datapath, original)
    im_dirs = os.listdir(all_museum_folders)

    for museum_folder in im_dirs:
        if museum_folder != ".DS_Store":
            folder_resize(os.path.join(datapath, original, museum_folder))

    new_images_dir = os.path.join(datapath, 'resized')
    return new_images_dir

