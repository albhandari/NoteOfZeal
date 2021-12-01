from website import db
from flask_login import UserMixin
from website import logging 


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))

class ToDoList(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    complete = db.Column(db.Boolean)

class Flashcard(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    owner = db.Column(db.String(64))
    fctitle = db.Column(db.String(64))
    fcterm =  db.Column(db.String(64))
    fcdesc = db.Column(db.String(5000))
    fcurl = db.Column(db.Integer)
    sharedwith = db.Column(db.String(64))

class Tracker(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    mostrecent = db.Column(db.Integer)
    secondrecent = db.Column(db.Integer) 
    thirdrecent = db.Column(db.Integer)
    logintime = db.Column(db.Integer)
    logouttime = db.Column(db.Integer)




@logging.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
