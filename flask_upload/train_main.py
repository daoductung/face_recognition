from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
from flask_upload.classifier import training


def train_data_image():
    datadir = './pre_img'
    modeldir = './model/20170511-185253.pb'
    classifier_filename = 'class/classifier.pkl'
    print("Training Start")
    obj = training(datadir, modeldir, classifier_filename)
    get_file = obj.main_train()
    if not get_file:
        return False
    print('Saved classifier model to file "%s"' % get_file)
    return True
