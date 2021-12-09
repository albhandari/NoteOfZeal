from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField

from wtforms.validators import InputRequired,DataRequired,  Email, Length



#for /login --> user to log in at login.html and /login
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min = 3, max = 30)])
    password = PasswordField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])
    submit = SubmitField('Sign in')


#for /signup --> user to sign up at signup.html and /signup
class SignupForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(),Email(message = 'Invalid email'), Length(max = 50)])
    username = StringField('Username', validators = [InputRequired(), Length(min = 3, max = 30)])
    password = PasswordField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])
    submit = SubmitField('Sign Up')


#For To Do List feature at todolist.html and /todolist
class ToDoListForm(FlaskForm):
    name = StringField('Enter a task', validators = [InputRequired()])
    addtask = SubmitField('Add task')


#for Blog located at blog.html and /blog
class BlogForm(FlaskForm):
    name = StringField('Enter blog title', validators = [InputRequired()])
    post = StringField('Enter blog post', validators = [InputRequired()])
    addPost = SubmitField('Add post')
    

#for Flashcards at /fccreate/<int> or at fccreate.html
class FlashCardForm(FlaskForm):
    fctitle = StringField('Title', validators = [InputRequired()])
    fcword = StringField('Term', validators = [InputRequired()])
    fcdef = StringField('Description', validators = [InputRequired()])
    addfc = SubmitField('Add')


#for Sharing which is located at /renderfc/<int> or at renderfc.html
class ShareForm(FlaskForm):
    sharedwith = StringField('Share with', validators = [InputRequired()])
    submit = SubmitField('Add User')


#located at navbar or at navbar.html
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators = [DataRequired()])
    submit = SubmitField("Submit")


#located at /makejournal or at makejournal.html
class JournalForm(FlaskForm):
    jtitle = StringField("Journal Title")
    jdesc = TextAreaField(validators = [InputRequired(), Length(max = 12081)])
    submit = SubmitField("Submit Entry")



