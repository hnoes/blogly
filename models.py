"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect the database to the FLask app"""
    
    db.app = app 

class User(db.Model):
    """User model"""

    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text(), unique=True, index=True,)
    image_url = db.Column(db.String(200), default='default_image.jpg') 


    def __repr__(self):
        """show info about user"""
        return f"<User '{self.id}', '{self.first_name}', '{self.last_name}'>"