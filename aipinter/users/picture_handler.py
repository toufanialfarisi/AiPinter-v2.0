import os
from PIL import Image
from flask import url_for, current_app

def add_profile_picture(pic_upload, username):
    filename = pic_upload.filename # pic_upload is in the form of flaskForm
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) +'.'+ext_type
    filepath = os.path.join(current_app.root_path, 'static\profile_pics')
    

    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thubmnail(output_size)
    spic.save(filepath)

    return storage_filename