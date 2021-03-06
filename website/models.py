from website import db
from flask_login import UserMixin
from website import logging 

 #user model for logging in and signing up
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))


#todolist model to store user's to-do-list
class ToDoList(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    name = db.Column(db.String(64))
    complete = db.Column(db.Boolean)

#Blog model for storing user's blogs
class Blog(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    title = db.Column(db.String(64))
    post = db.Column(db.String(64)) 
  
#Flashcard model to store Flashcard and it's terms
class Flashcard(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    owner = db.Column(db.String(64))
    fctitle = db.Column(db.String(64))
    fcterm =  db.Column(db.String(64))
    fcdesc = db.Column(db.String(5000))
    fcurl = db.Column(db.Integer)

#Tracking the progress bar for progress bar
class Tracker(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    logintime = db.Column(db.Integer)
    logouttime = db.Column(db.Integer)
    minutes = db.Column(db.Integer)

#tracks each Flashcard and which user it's shared to
class Sharing(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    owner = db.Column(db.String(64))
    title = db.Column(db.String(64))
    cardnumber = db.Column(db.Integer)
    sharedwith = db.Column(db.String(64))

#Stores user's journals
class Journal(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    owner = db.Column(db.String(64))
    jtitle = db.Column(db.String(64))
    jdesc =  db.Column(db.String(12081))
    jdate = db.Column(db.String())


@logging.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
