from flask_wtf import FlaskForm
from wtforms import StringField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
class Post(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Post')