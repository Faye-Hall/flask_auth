"""Models for Auth app"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Users(db.Model):
    
    __tablename__ = "users"

    username = db.Column(db.Text, nullable = False, primary_key= True)

    password = db.Column(db.Text, nullable = False)

    email = db.Column(db.Text, nullable = False)

    first_name = db.Column(db.Text, nullable = False)

    last_name = db.Column(db.Text, nullable = False)

    feedback = db.relationship("Feedback", backref="users", cascade="all,delete")
    
    @classmethod
    def register(cls,username,password, email, first_name, last_name):
        """Register user w/hased password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')
        
        user = cls (username = username, password = hashed_utf8 , email = email,first_name = first_name, last_name = last_name)
        
        #return instance of user with hashed pwd)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """ Validate that user exists & password is correct. Return user if valid; else return False."""

        user = Users.query.filter_by(username = username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            
            return user
        
        else:
            return False


class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer, nullable = False, primary_key= True, autoincrement= True ) 
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False) 
    username = db.Column(db.Text, db.ForeignKey('users.username'), nullable = False) 