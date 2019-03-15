from flask import redirect, url_for, render_template, Blueprint, flash
from aipinter.blogpost.forms import Post
from aipinter import db
from aipinter.models import BlogPost
from flask_login import current_user, login_required

blogpost = Blueprint('blogpost', __name__)

@blogpost.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    if current_user.is_authenticated:
        form = Post()
        if form.validate_on_submit():
            post = BlogPost(author=form.author.data, title=form.title.data,content=form.content.data)
            db.session.add(post)
            db.session.commit()
            flash('new post was added', 'success')
            return redirect(url_for('core.index'))
        return render_template('post.html', form=form)
    else:
        return redirect(url_for('login'))