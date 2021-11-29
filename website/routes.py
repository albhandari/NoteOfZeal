from website import myobj
from flask import render_template, flash, redirect
from flask_bootstrap import Bootstrap

@myobj.route("/home")
def home():
    return render_template('home.html')
