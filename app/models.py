from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    blogs = db.relationship('BlogPost', backref='author', lazy=True)
    status = db.Column(db.Boolean, default=True)
    login_dt = db.Column(db.DateTime, nullable=True)
    created_dt = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"User('{self.email}')"

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BlogPost('{self.title}', '{self.timestamp}')"
