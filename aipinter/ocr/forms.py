from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class OCRForm(FlaskForm):
    picture = FileField('Upload image', validators=[DataRequired()])
    description = TextAreaField('Description of image', validators=[DataRequired()])
    submit = SubmitField('Predict', validators=[DataRequired()])