from flask import redirect, url_for, render_template, Blueprint, flash, request
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
        return redirect(url_for('core.login'))

@blogpost.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    form = Post()
    post = BlogPost.query.get(id)
    if request.method == 'POST':
        post.author = request.form['author']
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.add(post)
        # db.session.flush()
        db.session.commit()
        flash('post suceessfull edited', 'success')
        return redirect(url_for('core.index'))
    else:
        return render_template('edit_post.html', form=form, post=post)

@blogpost.route('/delete/<int:id>', methods=['POST','GET'])
@login_required
def delete(id):
    post = BlogPost.query.filter_by(id_post=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Post successfully deleted', 'success')
    return redirect(url_for('core.index'))

@blogpost.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    searchForm = SearchForm()
    post = Post_article.query

    if searchForm.validate_on_submit():
        post = post.filter(Post_article.title.like('%' + searchForm.search.data + '%'))

        post = post.order_by(Post_article.title).all()
        return render_template('search_list.html', posts = post, form = searchForm)
    else:
        return render_template('search.html', form = searchForm)