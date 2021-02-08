# class for register model
from db import db

from datetime import datetime



# class for register model

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    useremail = db.Column(db.String(200), nullable=False , unique= True)
    userpassword = db.Column(db.String(900), nullable=False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return  "<Task %r>" % self.id

# class for flower model

class flowerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writtenflowername = db.Column(db.String(200), nullable=False)
    flowerdescription = db.Column(db.String(200), nullable=False)
    originalflowerimagename = db.Column(db.Text, unique=True, nullable=False)
    flower_date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return  "<Task %r>" % self.id

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

