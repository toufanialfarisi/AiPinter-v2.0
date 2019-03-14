from aipinter.models import ImageFile
from aipinter.vision.vision_handler import vision_utility
from aipinter.vision.forms import ComputerVisionForm
from flask_login import current_user
from flask import Blueprint, render_template, url_for, redirect, request, flash
from aipinter import app, ALLOWED_EXTENSIONS, secure_filename
import os
import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2
from aipinter import db
import shutil

vision = Blueprint('vision', __name__)

global graph 
graph = tf.get_default_graph()

@vision.route('/vision_list')
def vision_list():
    container = ImageFile.query.all()
    return render_template('vision_list.html', container=container)

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

@vision.route('/cvision', methods=['POST', 'GET'])
def cvision():
    form = ComputerVisionForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']
        file2 = request.files['kerasfile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file2.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            a = os.path.join(os.getcwd() + '/aipinter/static/image_vision', filename)
            file.save(a)
            # flash('upload success', 'success')

            image = filename
            model = file2.filename
            model_dir = os.path.join(os.getcwd() +'/aipinter/static/image_model', model)
            file2.save(model_dir)

            image_size = form.imagesize.data
            with graph.as_default():
                model = load_model(model_dir)
                # img = np.array(image)
                img = cv2.imread(image)
                img_ = cv2.resize(img, (image_size, image_size))
                pred_val, pred_class = pred_processing(model, img_)
                pred_val = pred_val[0]
                pred_class = pred_class[0]
                        
            user = ImageFile(image_file=a, description=form.description.data, prediction_val=pred_val, prediction_class=pred_class)
            db.session.add(user)
            db.session.commit()
            flash('Dideteksi = ' + str(pred_class) + ' , confidence = '+str(pred_val * 100)+' %', 'success')
            # except TypeError:
                # flash('predict result = ' + str(form.description.data), 'success')
            

        return redirect(url_for('vision.cvision',
                                    filename=filename))
    return render_template('cvision.html', form=form)
