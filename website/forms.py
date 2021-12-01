from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import InputRequired,DataRequired,  Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min = 3, max = 15)])
    password = PasswordField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])
    submit = SubmitField('Sign in')

class SignupForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(),Email(message = 'Invalid email'), Length(max = 50)])
    username = StringField('Username', validators = [InputRequired(), Length(min = 3, max = 15)])
    password = PasswordField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])
    submit = SubmitField('Sign Up')

class ToDoListForm(FlaskForm):
    name = StringField('Enter a task', validators = [InputRequired()])
    addtask = SubmitField('Add task')

class FlashCardForm(FlaskForm):
    fctitle = StringField('Title', validators = [InputRequired()])
    fcword = StringField('Term', validators = [InputRequired()])
    fcdef = StringField('Description', validators = [InputRequired()])
    addfc = SubmitField('Add')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators = [DataRequired()])
    submit = SubmitField("Submit")





