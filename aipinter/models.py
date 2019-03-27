from aipinter import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    # posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash, password)

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

    def __repr__(self):
        return f"UserName: {self.username}"


class BlogPost(db.Model):

    __tablename__ = 'blogpost'

    id_post = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(20), unique=False, nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)


    def __repr__(self):
        return f"ImageFile('{self.image_file}', '{self.description}')"


# class BlogPost(db.Model):
#     # Setup the relationship to the User table
#     users = db.relationship(User)

#     # Model for the Blog Posts on Website
#     id = db.Column(db.Integer, primary_key=True)
#     # Notice how we connect the BlogPost to a particular author
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     title = db.Column(db.String(140), nullable=False)
#     text = db.Column(db.Text, nullable=False)

#     def __init__(self, title, text, user_id):
#         self.title = title
#         self.text = text
#         self.user_id =user_id


#     def __repr__(self):
#         return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"



class ImageFile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image_file = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    prediction_val = db.Column(db.Float, unique=False, nullable=True)
    prediction_class = db.Column(db.String(20), unique=False, nullable=True)

    def __init__(self, image_file, description, prediction_val, prediction_class):
        self.image_file = image_file
        self.description = description
        self.prediction_val = prediction_val
        self.prediction_class = prediction_class

    def __repr__(self):
        return f"image_file : {self.image_file} , img : {self.image_file}"


class OCR(db.Model):

    __tablename__ = 'ocr'

    id = db.Column(db.Integer, primary_key = True)
    image_file = db.Column(db.String(20), unique=False)
    ocr_out = db.Column(db.String(50), unique=False)
    description = db.Column(db.Text, unique=False)

    def __init__(self, image_file, ocr_out, description):
        self.image_file = image_file
        self.ocr_out = ocr_out
        self.description = description
    
    def __repr__(self):
        return f"image_file : {self.image_file}, description {self.description}"

class Forecasting(db.Model):

    __tablename__ = 'forecasting'

    id = db.Column(db.Integer, primary_key=True)
    suhu_minimum = db.Column(db.Float)
    suhu_maksimum = db.Column(db.Float)
    suhu_rata_rata = db.Column(db.Float)
    kelembapan_rata2x = db.Column(db.Float)
    curah_hujan = db.Column(db.Float)
    lama_penyinaran = db.Column(db.Float)
    kecepatan_angin_rata2x = db.Column(db.Float)
    arah_angin_terbanyak = db.Column(db.Float)
    kecepatan_angin_terbesar = db.Column(db.Float)
    arah_angin_saat_max = db.Column(db.Float)

    def __repr__(self):
        return f"data with suhu minimum = {self.suhu_minimum} was added"

    

    








    