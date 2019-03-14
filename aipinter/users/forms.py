from flask_wtf import FlaskForm
from flask import Flask
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileStorage
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, IntegerField, SelectField
from wtforms.validators import Email, DataRequired, Length, EqualTo
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from aipinter.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('remember')
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, field):

        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered !')
    
    def validate_username(self,field):

        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is registered !')

class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


