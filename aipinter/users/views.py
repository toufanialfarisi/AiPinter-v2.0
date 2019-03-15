from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from aipinter.models import User, BlogPost
from aipinter.users.forms import RegisterForm, LoginForm, UpdateUserForm
from aipinter import db

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST', 'GET'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, 
        username=form.username.data, 
        password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['POST', 'GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
        
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
        # if check_password_hash(user.password, form.password.data) and user is

            login_user(user)
            flash('login success', 'success')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')
            
            return redirect(next)
    return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

# @user.route('/account', methods=['POST', 'GET'])
# def account():

#     form = UpdateUserForm()

#     if form.validate_on_submit():
        