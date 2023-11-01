from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(64), primary_key = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(16), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)

    posts = db.relationship("Post", backref="author")


    def __init__(self, first_name, last_name, username, password):
        self.id = str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)

    def compare_password(self, password):
        return check_password_hash(self.password, password)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "password":
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "posts": [post.to_response() for post in self.posts],
        }


class Post(db.Model):
    id = db.Column(db.String(64), primary_key = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    img_url = db.Column(db.String)
    title = db.Column(db.String(64), unique = True, nullable = False)
    caption = db.Column(db.Text)
    created_by = db.Column(db.String(64), db.ForeignKey("user.id"), nullable = False)


    def __init__(self, img_url, title,  caption, created_by):
        self.id = str(uuid4())
        self.img_url = img_url
        self.title = title
        self.caption = caption
        self.created_by = created_by
        
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "img_url": self.img_url,
            "title": self.title,
            "caption": self.caption,
            "created_by": self.created_by,
        }

