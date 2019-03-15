from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class ObjectDetectionForm(FlaskForm):
    choose_cam = SelectField('Object detection type ')
    submit = SubmitField('choose')