import os
import numpy as np
from PIL import Image
from flask import render_template, redirect, url_for
from aipinter import app, ALLOWED_EXTENSIONS, secure_filename


def vision_utility(image_file, model_file):
    image_filename = image_file.filename
    model_filename = model_file.filename

    path_image = os.path.join(os.getcwd(),'aipinter/static/image_vision', image_filename)
    path_model = os.path.join(os.getcwd(),'aipinter/static/image_model', str(model_filename))

    image_data = Image.open(path_image)
    image_data.save(path_image)

    return image_data, path_model, path_image


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def pred_processing(model, x_test, class_line=0.5):
    x_test = np.expand_dims(x_test, axis = 0)
    pred_result = model.predict(x_test)
    result = []
    for pred in pred_result:
        if pred < class_line:
            pred = 0
            result.append(pred)
        else:
            pred = 1
            result.append(pred)
    # result = np.asarray(result, dtype=np.int32)
    to_category = []
    for cat in result:
        if cat is 0:
            to_cat = 'Negatif Retak'
            to_category.append(cat)
        else:
            to_cat = 'Positive Retak'
            to_category.append(to_cat)
    return result, to_category

    

