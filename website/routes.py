from website import myobj, db
from website.models import User, ToDoList, Flashcard
from flask import render_template, flash, redirect, url_for, request
from website.forms import LoginForm, SignupForm, ToDoListForm, FlashCardForm, SearchForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from random import randint



@myobj.route("/")
@login_required
def mainMenu():
    return redirect(url_for('login'))



@myobj.route("/home")
@login_required
def home():
    displaylist.clear() 
    flashcardurl = uniqueurl()
    url = f'/makeflashcards/{flashcardurl}'

    thelist = listofurls()

    return render_template('home.html', url = url, thelist = thelist)

@myobj.route("/flashboard")
@login_required
def flashboard():
    displaylist.clear() 
    flashcardurl = uniqueurl()
    url = f'/makeflashcards/{flashcardurl}'

    thelist = listofurls()



    return render_template('flashboard.html', url = url, thelist = thelist)

@myobj.route("/deleteacc")
@login_required
def deleteacc():

    currentUser = User.query.filter_by(id=current_user.id).first()
    logout_user()
    db.session.delete(currentUser)
    db.session.commit()
    flash(f'User has been deleted')

    return redirect(url_for('login'))

@myobj.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = False)
                return redirect(url_for('home'))

        flash(f'Invalid username or password')
    return render_template('login.html', form = form)

@myobj.context_processor
def base():
    form = SearchForm()
    return dict(form=form)



@myobj.route('/search', methods = ['GET',"POST"])
def search():
    form = SearchForm()
    flashcards = Flashcard.query
    if form.validate_on_submit():
        form.searched = form.searched.data
        templist = similarity(form.searched)
        
        return render_template('search.html', form = form, searched = form.searched, templist = templist)



@myobj.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@myobj.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()


    if form.validate_on_submit():
        hashedpassword = generate_password_hash(form.password.data, method = 'sha256')
        newUser = User(username = form.username.data, email = form.email.data, password = hashedpassword)
        db.session.add(newUser)
        db.session.commit()

        flash(f"Login with your newly created account")

        return redirect ('/login')



    return render_template('signup.html', form = form)

@myobj.route('/todolist', methods = ['GET', 'POST'])
def todotlist():
    form = ToDoListForm()
    title = "To do list"
    if request.method == 'POST':
        content = request.form['name']
        newtask = ToDoList(name = content)
        try:
            db.session.add(newtask)
            db.session.commit()
            return redirect('/todolist')
        except:
            return flash('Error')
    else:
        tasks = ToDoList.query.all()
        return render_template('todolist.html', tasks = tasks, form = form, title = title)


@myobj.route('/delete/<int:id>')
def delete(id):
    delete_task = ToDoList.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect ('/todolist')
    except:
        return flash ('Error')


displaylist = []
@login_required
@myobj.route('/makeflashcards/<int:num>', methods = ['GET', 'POST'])
def makeflashcards(num):
    form = FlashCardForm()
    
    if form.validate_on_submit():  #if the user creates a new flashcard
        flashcard = Flashcard(owner = current_user.username, fctitle = form.fctitle.data, fcterm = form.fcword.data, fcdesc = form.fcdef.data, fcurl = num, sharedwith = 'admin')
        db.session.add(flashcard)
        db.session.commit()

        displaylist.append({'term' : form.fcword.data, 'definition' : form.fcdef.data})
    
    return render_template('fccreate.html', form = form, displaylist = displaylist)


@login_required
@myobj.route('/renderfc/<int:num>')
def renderfc(num):
    templist = []
    flashcards = Flashcard.query.filter_by(fcurl = num).all()
    for flashcard in flashcards:
        title = flashcard.fctitle
        templist.append({'term': flashcard.fcterm, 'description':flashcard.fcdesc})
    



    return render_template('renderfc.html', title = title, templist = templist)



def fourdigitcombo():
    return (1000 * randint(0,9)) + (100 *randint(0,9)) +  (10 * randint(0,9)) + randint(0,9)

def inthedatabase(num):
    return  db.session.query(db.exists().where(Flashcard.fcurl == num)).scalar()

def uniqueurl():
    finalnum = fourdigitcombo()
    while(inthedatabase(finalnum)):
        finalnum = fourdigitcombo()
    return finalnum

def listofurls():
    templist = []
    flashcards = Flashcard.query.filter_by(owner = current_user.username).all()
    for flashcard in flashcards:
        templist.append({'url': flashcard.fcurl, 'title':flashcard.fctitle})
    
    noduplicates = []
    for items in templist:
        if items not in noduplicates:
            noduplicates.append(items) 
    
    return noduplicates

def similarity(phrase):
    templist = []
    flashcards = Flashcard.query.filter_by(owner = current_user.username).all()
    for flashcard in flashcards:
        if(phrase in flashcard.fctitle or phrase in flashcard.fcdesc):
            templist.append({'url': flashcard.fcurl, 'title':flashcard.fctitle})
    
    noduplicates = []
    for items in templist:
        if items not in noduplicates:
            noduplicates.append(items) 
    
    return noduplicates
    

    

