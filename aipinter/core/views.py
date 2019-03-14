from flask import render_template, url_for, redirect, Blueprint
from aipinter.core.forms import SearchForm
core = Blueprint('core', __name__)

@core.route('/')
def index():
    form = SearchForm()
    return render_template('home.html', form=form)