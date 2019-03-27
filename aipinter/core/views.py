from flask import render_template, url_for, redirect, Blueprint, jsonify
from aipinter.core.forms import SearchForm
from aipinter.models import BlogPost
from aipinter import db
from aipinter.schema import UserPostSchema
from flask_login import login_required

core = Blueprint('core', __name__)

@core.route('/', methods=['POST', 'GET'])
def index():
    searchForm = SearchForm()
    post = BlogPost.query.all()
    # db.session.commit()
    post1 = BlogPost.query.all()
    post = BlogPost.query

    if searchForm.validate_on_submit():
        post = post.filter(BlogPost.title.like('%' + searchForm.search.data + '%'))

        post = post.order_by(BlogPost.title).all()
        return render_template('search_list.html', posts = post, form = searchForm)
    else:
        return render_template('home.html', title='Home',mypost=post1, form = searchForm)
    

    return render_template('home.html', title='Home', mypost=post1) 
    return render_template('home.html', form=form, mypost=post)


@core.route('/api/post', methods=['GET', 'POST'])
@login_required
def api():
    blog = BlogPost.query.all()
    user_schema = UserPostSchema(many=True)
    output = user_schema.dump(blog).data
    return jsonify(output)


