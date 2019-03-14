from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ComputerVisionForm(FlaskForm):
    modelkeras = FileField('Upload Keras Model', validators=[DataRequired()])
    imagesize = IntegerField('Image size (width = height)', validators=[DataRequired()])
    picture = FileField('Upload image', validators=[DataRequired()])
    description = TextAreaField('Description of image', validators=[DataRequired()])
    submit = SubmitField('Predict', validators=[DataRequired()])