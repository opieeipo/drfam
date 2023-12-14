from flask_login import UserMixin
from . import db


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    usertype = db.Column(db.String(10), default='standard' )

  

class Query(db.Model):
    __tablename__ = "queries"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))    
    query = db.Column(db.String(1000))
    response = db.Column(db.String(1000))
    duration = db.Column(db.Integer)
    reference = db.Column(db.String(1000))

 
