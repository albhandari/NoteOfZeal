from website import myobj, db
from website.models import User, ToDoList, Flashcard
from flask import render_template, flash, redirect, url_for, request
from website.forms import LoginForm, SignupForm, ToDoListForm, FlashCardForm, SearchForm, UploadFileForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from random import randint
from werkzeug.utils import secure_filename
#initial page when loading up is redirected to login-page
@myobj.route("/")
@login_required
def mainMenu():
    return redirect(url_for('login'))


#home page
@myobj.route("/home")
@login_required
def home():

    #clears flashcards from /makeflashcards
    #so there isn't visual conflict
    displaylist.clear() 
    flashcardurl = uniqueurl()                  #url for each specific flashcard
    url = f'/makeflashcards/{flashcardurl}'

    thelist = listofurls()

    return render_template('home.html', url = url, thelist = thelist)


#page for all the flashcards related implementation
@myobj.route("/flashboard")
@login_required
def flashboard():
    displaylist.clear() 
    flashcardurl = uniqueurl()
    url = f'/makeflashcards/{flashcardurl}'

    thelist = listofurls()



    return render_template('flashboard.html', url = url, thelist = thelist)


#uses current_User from flask_login to get current User id and removes from the sqldatabase
@myobj.route("/deleteacc")
@login_required
def deleteacc():

    currentUser = User.query.filter_by(id=current_user.id).first()
    logout_user()
    db.session.delete(currentUser)
    db.session.commit()
    flash(f'User has been deleted')

    return redirect(url_for('login'))


#simple login implementation, even hashes the password in the database
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


#wrapper to tell where to locate the form in NAV bar 
@myobj.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


#When clicked on the search on nav bar, redirects to /search to find the flashcard related to user's search term
@myobj.route('/search', methods = ['GET',"POST"])
def search():
    form = SearchForm()
    flashcards = Flashcard.query
    if form.validate_on_submit():
        form.searched = form.searched.data
        templist = similarity(form.searched)
        
        return render_template('search.html', form = form, searched = form.searched, templist = templist)


#Logs user out
@myobj.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#basic signup and uses hashpassword to store data too
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


#To-do list that allows user to store bullet point list
#which they can check off and will be removed from the database
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

#deletes task that user inputted
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

#Rendering the PROCESS of making flash card
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


#rendering the flash card by getting the url, then by publishing it with different templates 
@login_required
@myobj.route('/renderfc/<int:num>')
def renderfc(num):
    templist = []
    flashcards = Flashcard.query.filter_by(fcurl = num).all()
    for flashcard in flashcards:
        title = flashcard.fctitle
        templist.append({'term': flashcard.fcterm, 'description':flashcard.fcdesc})
    



    return render_template('renderfc.html', title = title, templist = templist)


#combination of numbers from 0-9 with 4 placeholders, for variety of distinct urls
def fourdigitcombo():
    return (1000 * randint(0,9)) + (100 *randint(0,9)) +  (10 * randint(0,9)) + randint(0,9)

#checks if the fourdigitcombo() is already in database
def inthedatabase(num):
    return  db.session.query(db.exists().where(Flashcard.fcurl == num)).scalar()

#after taking in input from fourdigitcombo() and 
def uniqueurl():
    finalnum = fourdigitcombo()
    while(inthedatabase(finalnum)):
        finalnum = fourdigitcombo()
    return finalnum

#returns urls of flashcards
#since some of the terms have the same url, it doesn't duplicate the url
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


#checks the phrase user inputted to find similar flash cards
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

@myobj.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@myobj.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
