from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sns_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)


# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))


# Routes
@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    content = request.form.get('content')
    username = request.form.get('username')

    if not content or not username:
        flash('Content and username are required!', 'error')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=username).first()

    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    new_post = Post(content=content, user_id=user.id)
    print(new_post)
    db.session.add(new_post)
    db.session.commit()
    flash('Post created successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('index'))
    
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

if __name__ == '__main__':
    db_path = 'instance/sns_app.db'
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001, host='0.0.0.0')
