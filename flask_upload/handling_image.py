from numpy import expand_dims
from keras.preprocessing.image import load_img, save_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from flask_upload.handling import *
import time


# path = '\\detect_3\\train_img/tung\\'


# Dinh nghia 1 doi tuong Data Generator voi bien phap chinh sua anh dieu chinh do sang tu 0.5% den 2.0%
def image_processes(file_img='', type = '', sl=2):
    if not file_img:
        return None
    img = load_img(file_img)
    img = img_to_array(img)
    data = expand_dims(img, 0)
    myImageGen = None
    if type == 'brightness':
        myImageGen = ImageDataGenerator(brightness_range=[0.5, 2.0])
    elif type == 'flip':
        myImageGen = ImageDataGenerator(horizontal_flip=True, vertical_flip=True)
    elif type == 'rotate':
        myImageGen = ImageDataGenerator(rotation_range=45)
    elif type == 'shear':
        myImageGen = ImageDataGenerator(shear_range=45)
    elif type == 'shift':
        myImageGen = ImageDataGenerator(width_shift_range=[-150,150])
    if not myImageGen:
        return False
    gen = myImageGen.flow(data, batch_size=1)
    for i in range(sl):
        myBatch = gen.next()
        image = myBatch[0].astype('uint8')
        name_folder, path, name, extension = get_name_and_path_by_path_image(file_img)
        img = get_path_image('train_img\\' + name_folder, name + str(time.time()).replace('.', '') + '_' + type + '.' + extension)
        save_img(img, image)
    return True


