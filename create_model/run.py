import sys
sys.path.insert(
    0,
    "./scripts/"
)
from images import training_resize
from model import train_and_save_model



def main():
    DATA_PATH = "./images/training/"
    original_folder = "original/"

    # Resize the original images to 224 x 224
    resized_folder_path = training_resize(DATA_PATH, original_folder)
    print("Done. Resized images are located here:\n{}".format(resized_folder_path))
    train_and_save_model(sys.argv[1:])
    
if __name__ == '__main__':
    main()