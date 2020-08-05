import glob
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
from PIL import ImageEnhance
from flask_upload.handling_image import *
import numpy as np
import cv2

data_paths = glob.glob("data_img/*")
train_paths = glob.glob("train_img/*")
# print(train_paths)

df_train = pd.DataFrame(columns=['image', 'label', 'name'])


def save_image_handling(data_paths=data_paths, train_paths=''):
    data_paths = glob.glob("data_img/*")
    # delete_folder_by_path(train_paths)
    for i, data_path in tqdm(enumerate(data_paths)):
        name = data_path.split("\\")[-1]
        images = glob.glob(data_path + "/*")
        for image in images:
            for tp in ['brightness', 'flip', 'rotate', 'shear', 'shift']:
                if not image_processes(image, tp):
                    continue
    return True


def get_df_train(df_train=df_train):
    train_paths = glob.glob("train_img/*")
    df_train = pd.DataFrame(columns=['image', 'label', 'name'])
    for i, train_path in tqdm(enumerate(train_paths)):
        name = train_path.split("\\")[-1]
        images = glob.glob(train_path + "/*")
        for image in images:
            df_train.loc[len(df_train)] = [image, i, name]
    return df_train


def extract_face(filename, required_size=(224, 224)):
    pixels = pyplot.imread(filename)
    detector = MTCNN()
    results = detector.detect_faces(pixels)
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    face = pixels[y1:y2, x1:x2]
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


def adjust_sharpness(input_image, output_image, factor):
    image = Image.open(input_image)
    # enhancer_object = ImageEnhance.Sharpness(image)
    # out = enhancer_object.enhance(factor)
    image.save(output_image.replace('png', 'jpg'))
    return output_image.replace('png', 'jpg')


def cut_image_face(df_train=df_train):
    for img_path in df_train.image:
        required_size = (182, 182)
        # x = adjust_sharpness(img_path, img_path, 1.7)
        pixels = pyplot.imread(img_path)
        detector = MTCNN()
        results = detector.detect_faces(pixels)
        if not results:
            continue
        x1, y1, width, height = results[0]['box']
        x2, y2 = x1 + width, y1 + height
        face = pixels[y1:y2, x1:x2]
        try:
            image = Image.fromarray(face)
            image = image.resize(required_size)
            face_array = asarray(image)

            name_folder, name_image, _, extension = get_name_and_path_by_path_image(img_path)
            pyplot.imsave(get_path_image('pre_img\\' + name_folder, name_image), face_array)
        except Exception as e:
            print(e)
    return True
