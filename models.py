"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS!
class User(db.Model):
    """Model for site user"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default='https://thearrivalstore.com/wp-content/uploads/2016/04/default_user_icon.jpg')

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Returns the user's full name"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Model for blog post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def formatted_date(self):
        """Return a formatted date representation useful for displaying"""
        return self.created_at.strftime("%c")

class PostTag(db.Model):
    """Model for join table b/w posts and tags"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Model for tags"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary="post_tags", backref="tags")