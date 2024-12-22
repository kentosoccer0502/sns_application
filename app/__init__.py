from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    
    db.init_app(app)

    from app.models.user import User
    from app.models.post import Post

    from app.routes.main import main
    app.register_blueprint(main)
    
    return app
