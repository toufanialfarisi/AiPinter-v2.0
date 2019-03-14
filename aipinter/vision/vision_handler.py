import os
from PIL import Image
from flask import render_template, redirect, url_for

def vision_utility(image_file, model_file):
    image_filename = image_file.filename
    model_filename = model_file.filename

    path_image = os.path.join(os.getcwd(),'aipinter/static/image_vision', image_filename)
    path_model = os.path.join(os.getcwd(),'aipinter/static/image_model', str(model_filename))

    image_data = Image.open(path_image)
    image_data.save(path_image)

    return image_data, path_model, path_image



    

