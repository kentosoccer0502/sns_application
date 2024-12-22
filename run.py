from app import create_app, db
from app.models.user import User
from app.models.post import Post


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

with app.app_context():
    db.create_all()  # データベーステーブルを作成