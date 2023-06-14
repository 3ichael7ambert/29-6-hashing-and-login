"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

    def to_dict(self):
        """Serialize user to a dict of user info."""
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
    
class Feedback(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    username = Column(String(100), ForeignKey('users.username'), nullable=False)

    user = relationship('User', backref='feedbacks')

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
