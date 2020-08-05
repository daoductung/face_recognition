import os
import calendar
import time
import re
import shutil


def get_root_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_root_path_file():
    return os.getcwd()


def create_folder_by_name(folder_name=None):
    if not folder_name:
        return None
    path = str(get_root_path_file()).rstrip('/') + '/' + str(folder_name).lstrip('/').rstrip('/') + '/'
    if not os.path.exists(path):
        os.makedirs(path)
        os.chmod(path, 0o777)
    return True


# def get_file_exits(path=None, file_name=None):
#     create_folder_by_name(path)
#     if not file_name:
#         return False
#     # if os.path.isfile(file_name):
#     #     delete_file_by_path(file_name)
#     return file_name


def delete_folder_by_path(path=None):
    if not path:
        return None
    if isinstance(path, list):
        for f in path:
            try:
                shutil.rmtree(get_root_path_file() +'\\'+ f.replace('/', ''))
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
            # os.rmdir(get_root_path_file() +'\\'+ f.replace('/', ''))

    else:
        os.rmdir(path)
    return True


def delete_file_by_path(path=None):
    if not path:
        return None
    os.remove(path)
    return True


def create_image_name(image='', prefix=None):
    if not image:
        return 'default.jpg'
    name_image = ''
    image_format = ['jpeg', 'jpg', 'png']
    if image.split('.')[-1] not in image_format:
        name_image = image + '.png'
    return name_image


def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def response_success(data='', msg=''):
    return {'status': 200, 'data': data, 'msg': msg}


def response_error(data='', msg=''):
    return {'status': 404, 'data': data, 'msg': msg}


def no_accent(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s.replace(' ', '_').lower()


# print(get_root_path_file())

# def get_root_path():
#     return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
#
# def get_root_path_file():
#     return os.getcwd()
#
#
# def create_folder_by_name(folder_name=None):
#     if not folder_name:
#         return None
#     path = str(get_root_path_file()).rstrip('/') + '/' + str(folder_name).lstrip('/').rstrip('/') + '/'
#     if not os.path.exists(path):
#         os.makedirs(path)
#         os.chmod(path, 0o777)
#     return True


def get_name_and_path_by_path_image(file_name=''):
    if not file_name:
        return None
    return file_name.split('\\')[-2], file_name.split('\\')[-1], file_name.split('\\')[-1].split('.')[0], \
           file_name.split('\\')[-1].split('.')[1]


def get_path_image(folder_name='', file_name=None):
    if not file_name:
        return None
    path = get_root_path_file() + '\\' + folder_name + '\\'
    if not os.path.exists(path):
        os.makedirs(path)
        os.chmod(path, 0o777)
    return path + '\\' + file_name


def get_file_exits(path=None, file_name=None):
    create_folder_by_name(path)
    if not file_name:
        return False
    # if os.path.isfile(file_name):
    #     return file_name.replace(file_name) + str(calendar.timegm(time.gmtime()))
    return file_name

#
# def delete_folder_by_path(path=None):
#     if not path:
#         return None
#     os.rmdir(path)
#     return True

# delete_folder_by_path('C:\\Users\\TungPC\\PycharmProjects\\project_nhat-master\\flask_upload\\train_img')