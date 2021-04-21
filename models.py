"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy() 

def connect_db(arr):
    db.app = arr 
    db.init_app(arr)


class User (db.Model):
    """User"""

    __tablename__ = "users"


    def __repr__(self):
        return f"user first name is {self.first_name} and last name is {self.last_name}, id {self.id}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(30),
                            nullable=False)

    last_name = db.Column(db.String(20),
                            nullable=False)

    image_url = db.Column(db.String,
                            nullable=False)

    def greeting(self):
        return f"Hi,my name is {self.first_name} {self.last_name}!"

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    def __repr__ (self):
        return f"Post id of {self.id},title of {self.title},user_id is {self.user_id}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.Text,nullable=False)

    content = db.Column(db.Text,nullable=False)

    created_at = db.Column(db.DateTime(9), default=datetime.now())

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    user = db.relationship('User',backref='posts',passive_deletes=True)

    post_tag = db.relationship("PostTag",backref="posts",passive_deletes=True)

    tag = db.relationship("Tag",secondary="post_tag",backref="posts",passive_deletes=True)

class Tag(db.Model): 
    """Tags"""

    __tablename__ = "tags"

    def __repr__ (self):
        return f"tag is {self.id} of {self.name}"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    name = db.Column(db.Text,nullable=False,unique=True)

    post_tag = db.relationship("PostTag",backref="tags",passive_deletes=True)

class PostTag(db.Model): 
    """Post Tag"""

    __tablename__ = "post_tag"

    def __repr__(self):
        return f"post_id is {self.post_id},tag_id is {self.tag_id}"

    post_id = db.Column(db.Integer,db.ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)

    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id",ondelete="CASCADE"),primary_key=True)
