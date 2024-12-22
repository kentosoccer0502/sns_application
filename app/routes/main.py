from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db

from app.models.user import User
from app.models.post import Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@main.route('/post', methods=['POST'])
def post():
    content = request.form.get('content')
    username = request.form.get('username')

    if not content or not username:
        flash('Content and username are required!', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(username=username).first()

    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    new_post = Post(content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()
    flash('Post created successfully!', 'success')
    return redirect(url_for('main.index'))

@main.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('main.index'))
    
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)
