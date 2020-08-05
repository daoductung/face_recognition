from flask import Flask, json, request, send_from_directory
from flask_cors import CORS
from PIL import Image
from io import BytesIO
from flask_upload.python_mysql.main import *
import base64
import pandas as pd
from flask_upload.handling import *
from flask_upload.face_detect_and_save import *
from flask_upload.train_main import *
from flask_upload.face_image import *
import glob
from datetime import datetime

data_paths = glob.glob("data_img/*")
train_paths = glob.glob("train_img/*")
train_path = glob.glob("train_img/")

df_train = pd.DataFrame(columns=['image', 'label', 'name'])

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# app.config['CORS_HEADERS'] = 'Content-Type'

table_user = {
    'ID': 'INT AUTO_INCREMENT PRIMARY KEY',
    'masv': 'Varchar(255)',
    'name': 'TEXT',
    'age': 'INT',
    'className': 'Varchar(255)',
    'address': 'Varchar(255)',
    'phone': 'Varchar(255)',
    'subject': 'Varchar(255)',
    'image_path': 'Varchar(255)',
    'id_data': 'Varchar(255)'
}

table_report_column = {
    'user_id': 'Varchar(255)',
    'created_at': 'datetime'
}

database_name = 'test'
table_name = 'face'
table_attendance = 'Attendance'
table_report = 'report'


def train_data():
    if save_image_handling(data_paths, train_path):
        x = get_df_train(df_train)
        cut_image_face(df_train=x)
        return train_data_image()
    return False


def face_detect(image_url=''):
    if not image_url:
        return response_error()
    if Recognition(image_url):
        return response_success(Recognition(image_url))
    return response_error()


def save_image_get_api(data_image=dict()):
    size_image = (800, 800)
    if not data_image.get('image') or data_image.get('type') not in ['train', 'test', 'check']:
        return False
    img_data = Image.open(BytesIO(base64.b64decode(str(data_image['image']).replace('data:image/png;base64,', ''))))
    img = img_data.resize(size_image)  # resize image 128 128
    name_image = data_image['name_image']
    if data_image.get('type') == 'train':
        path_root_img = 'data/' + data_image['name_folder'] + '/'
        path_train_img = 'data_img/' + data_image['name_folder'] + '/'
        img_data.save(get_file_exits(path_root_img, path_root_img + name_image))
        img_data.save(get_file_exits(path_train_img, path_train_img + name_image))

        im1 = Image.open(path_train_img + name_image)
        img1 = im1.convert('RGB')
        img1.save(path_train_img + name_image.replace('png', 'jpg'))
        delete_file_by_path(get_file_exits(path_train_img, path_train_img + name_image))
        return get_file_exits(path_root_img, path_root_img + name_image)
    if data_image.get('type') == 'test':
        path_root_img = 'data/' + data_image['name_folder'] + '/'
        # path_train_img = 'data_img/' + data_image['name_folder'] + '/'
        img_data.save(get_file_exits(path_root_img, path_root_img + name_image))
        # img_data.save(get_file_exits(path_train_img, path_train_img + name_image))
        return get_file_exits(path_root_img, path_root_img + name_image)
    return False


def import_data_table_report(data_import=dict()):
    if not mysql_execute().check_database(database_name):
        mysql_execute().create_database(database_name)
    if not mysql_execute().check_table(database_name, table_report):
        mysql_execute().create_table(database_name, table_report, column_data=table_report_column)
    report_id = mysql_execute().insert_data_row(database_name, table_report, data_import)
    return report_id


@app.route('/getAll', methods=['POST', 'GET'])
def getAll():
    all_std = mysql_execute().select_data(database_name, table_name)
    for std in all_std:
        if 'image_path' in std:
            std['image'] = 'http://127.0.0.1:9898/uploads/' + std['image_path']

    return json.dumps(all_std)


@app.route('/image', methods=['POST', 'GET'])
def image():
    data = request.get_json()
    if data:
        save_image_get_api(data)
    return json.dumps(list())


@app.route('/add', methods=['POST', 'GET'])
def add():
    data = request.get_json()
    if data:
        if not mysql_execute().check_database('test'):
            mysql_execute().create_database('test')
        if not mysql_execute().check_table('test', 'face'):
            mysql_execute().create_table('test', 'face', column_data=table_user)
        if 'path' not in data:
            data['path'] = no_accent(data['name'])
        data['image_path'] = ''
        data['type'] = 'train'
        data['name_image'] = data['path'] + '.png'
        data['name_folder'] = data['path'] + '_' + str(int(time.time()))
        data['Id_Data'] = data['name_folder']
        if save_image_get_api(data):
            data['image_path'] = save_image_get_api(data)
        for key in ['image', 'path', 'type', 'name_image', 'name_folder']:
            if key in data:
                del data[key]
        user_id = mysql_execute().insert_data_row('test', 'face', data)
        if user_id:
            mysql_execute().update_data('test', 'face', {'masv': 'MSV' + str(user_id)}, {'ID': user_id})
            return json.dumps(response_success(user_id))
    return json.dumps(response_error())


@app.route('/edit/<user_id>', methods=['POST', 'GET'])
def edit(user_id):
    data = request.get_json()
    if data and user_id:
        data['image_path'] = ''
        if 'path' not in data:
            data['path'] = no_accent(data['name'])
        data['type'] = 'train'
        data['name_image'] = data['path'] + '.png'
        user_data = mysql_execute().select_data(database_name, table_name, {'id': user_id})
        if user_data:
            data['path'] = user_data[0]['id_path']
        data['name_folder'] = data['path']
        if save_image_get_api(data):
            data['image_path'] = save_image_get_api(data)
        for key in ['image', 'path', 'type', 'name_image', 'name_folder']:
            if key in data:
                del data[key]
        update_user = mysql_execute().update_data(database_name, table_name, data, {'id': user_id})
        if update_user:
            return response_success(user_id)
    return response_error()


@app.route('/delete/<user_id>', methods=['POST', 'GET'])
def delete(user_id):
    if user_id:
        user_data = mysql_execute().select_data(database_name, table_name, {'id': user_id})
        if user_data:
            delete_folder_by_path(['data_img\\' + user_data[0]['id_path'], 'data\\' + user_data[0]['id_path']])
        delete_user = mysql_execute().delete_data(database_name, table_name, {'id': user_id})
        if delete_user:
            return response_success(user_id)
    return response_error()


@app.route('/uploads/data/<folder>/<filename>')
def uploaded_file(folder, filename):
    folder = get_root_path_file() + '\\data\\' + folder
    x = send_from_directory(folder, filename)
    return x


@app.route('/train', methods=['POST', 'GET'])
def train():
    delete_folder_by_path(['train_img', 'pre_img'])
    if not train_data():
        return response_error('Hình ảnh train cần bao gồm khuôn mặt rõ nét của bạn!')
    return response_success()


@app.route('/result', methods=['POST', 'GET'])
def result():
    result_data = None
    data = request.get_json()
    if data:
        data['image_path'] = ''
        data['type'] = 'test'
        data['name_image'] = data['name_image']
        data['name_folder'] = data['name_folder']
        if save_image_get_api(data):
            x = save_image_get_api(data)
            result_data = Recognition(save_image_get_api(data))
        if not result_data:
            return json.dumps([{'masv': int(time.time()), 'name': 'unknow',
                                'created_at': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}])
        all_result = list()
        if result_data:
            result_select = mysql_execute().select_data(database_name, table_name, {'Id_Data': result_data})
            for std in result_select:
                if 'image_path' in std:
                    std['image'] = 'http://127.0.0.1:9898/uploads/' + std['image_path']
                    std['image_new'] = 'http://127.0.0.1:9898/uploads/' + x
                    created_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    std['created_at'] = created_at
                    import_data_table_report({"user_id": std['id'], 'created_at': created_at})
                    all_result.append(std)

            return json.dumps(all_result)

    return response_success()


@app.route('/report', methods=['POST', 'GET'])
def report():
    data = request.get_json()
    if data:
        all_results = list()
        if not mysql_execute().check_database(database_name) or not mysql_execute().check_table(database_name,
                                                                                                table_report):
            return response_error('Không thể kết nối được database')
        data_reports = mysql_execute().select_data_report(database_name, data)
        if data_reports:
            user_ids = [x['user_id'] for x in data_reports]
            result_select = mysql_execute().select_data(database_name, table_name, {'id': user_ids})
            for std in result_select:
                for report in data_reports:
                    if int(report['user_id']) == int(std['id']):
                        std['created_at'] = report['created_at']
                all_results.append(std)

            return json.dumps(all_results)
    return json.dumps(list())


if __name__ == '__main__':
    app.run(debug=True, port='9898')
