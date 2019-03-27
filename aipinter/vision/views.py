from __future__ import print_function, division, absolute_import

from aipinter.models import ImageFile
from aipinter.vision.vision_handler import vision_utility, allowed_file, pred_processing
from aipinter.vision.forms import ComputerVisionForm
from flask_login import current_user, login_required
from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify
from aipinter import app, ALLOWED_EXTENSIONS, secure_filename
import os
import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2
from aipinter import db
from aipinter.schema import ImageFileSchema
import shutil

tf.logging.set_verbosity(tf.logging.ERROR)

vision = Blueprint('vision', __name__)
# vision_api = Blueprint()

global graph 
graph = tf.get_default_graph()


@vision.route('/cvision', methods=['POST', 'GET'])
@login_required
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
            image_path = os.path.join(os.getcwd() + '/aipinter/static/image_vision', filename)
            file.save(image_path)
            # flash('upload success', 'success')



            image = image_path
            model = file2.filename
            model_dir = os.path.join(os.getcwd() +'/aipinter/static/image_model', model)
            file2.save(model_dir)

            image_size = form.imagesize.data
            with graph.as_default():
                model = load_model(model_dir)
                # img_ = np.array(image)
                img = cv2.imread(image)
                img_ = cv2.resize(img, (image_size, image_size))
                pred_val, pred_class = pred_processing(model, img_)
                pred_val = pred_val[0]
                pred_class = pred_class[0]

            # image_path = image_path.split('/')[-2:]                        
            user = ImageFile(image_file=image_path, description=form.description.data, prediction_val=pred_val, prediction_class=pred_class)
            

            db.session.add(user)
            db.session.commit()
            flash('Dideteksi = ' + str(pred_class) + ' , confidence = '+str(pred_val * 100)+' %', 'success')
            return render_template('cvision.html', form=form, file_url=image_path, filename=filename, os=os)
            # except TypeError:
                # flash('predict result = ' + str(form.description.data), 'success')
            

        return redirect(url_for('vision.cvision',
                                    filename=filename))
    return render_template('cvision.html', form=form)

@vision.route('/vision_list')
@login_required
def vision_list():
    container = ImageFile.query.all()
    try:
        one_cont = ImageFile.query.first()
        return render_template('vision_list.html', container=container, os=os, post=one_cont.id)
    except:
        flash('No Image Available', 'danger')
        return render_template('vision_list.html', container=container, os=os, post=None)


@vision.route('/vision_list/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def vision_delete(id):
    vis = ImageFile.query.filter_by(id=id).first()
    # container = ImageFile.query.all()
    db.session.delete(vis)
    db.session.commit()
    flash('image was successfully deleted', 'success')
    return redirect(url_for('vision.vision_list'))




@vision.route('/api/vision')
@login_required
def vision_list_api():
    container = ImageFile.query.all()
    schema = ImageFileSchema(many=True)
    output = schema.dump(container).data
    return jsonify(output)
