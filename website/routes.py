import datetime
from website import myobj, db
from website.models import User, ToDoList, Flashcard, Sharing, Tracker, Blog
from flask import render_template, flash, redirect, url_for, request, session
from website.forms import LoginForm, SignupForm, ToDoListForm, FlashCardForm, SearchForm, ShareForm, BlogForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from random import randint
from flaskext.markdown import Markdown
from werkzeug.utils import secure_filename
import markdown.extensions.fenced_code

login_utc = datetime.datetime.utcnow()
logout_utc = datetime.datetime.utcnow()
#initial page when loading up is redirected to login-page
@myobj.route("/")
def mainMenu():
    return render_template('index.html')


#home page
@myobj.route("/home")
@login_required
def home():

    #clears flashcards from /makeflashcards
    #so there isn't visual conflict
    displaylist.clear() 
    flashcardurl = uniqueurl()                  #url for each specific flashcard
    url = f'/makeflashcards/{flashcardurl}'
    owner = current_user.username

    thelist = listofurls()

    return render_template('home.html', url = url, thelist = thelist, owner = owner)

#home page
@myobj.route("/error")
@login_required
def error():

    #clears flashcards from /makeflashcards
    #so there isn't visual conflict
    displaylist.clear() 
    flashcardurl = uniqueurl()                  #url for each specific flashcard
    url = f'/makeflashcards/{flashcardurl}'
    owner = current_user.username

    thelist = listofurls()

    return render_template('error.html', url = url, thelist = thelist, owner = owner)


#page for all the flashcards related implementation
@myobj.route("/flashboard")
@login_required
def flashboard():
    displaylist.clear() 
    flashcardurl = uniqueurl()
    url = f'/makeflashcards/{flashcardurl}' 

    thelist = listofurls() #user's own flashcard
    sharedlist = sharedFlashCardslist()



    return render_template('flashboard.html', url = url, thelist = thelist, sharedlist = sharedlist)


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
    color = "green"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = False)
                login_utc = datetime.datetime.utcnow()
                return redirect(url_for('home'))

        flash(f'Invalid username or password')
    return render_template('login.html', form = form, color = color)


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
    logout_utc = datetime.datetime.utcnow()
    sessionmins = Tracker(username = current_user.username, logintime = login_utc, logouttime = logout_utc, minutes = totalminutes(login_utc, logout_utc))
    db.session.add(sessionmins)
    db.session.commit()
    logout_user()
    flash(f'You have successfully logged-out!')
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
@login_required
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
            return redirect('/error')
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
        return redirect('/error')

displaylist = []

@myobj.route('/blog', methods=['GET', 'POST'])
@login_required

def blog():
    form=BlogForm()
    title="Blog posts"
    if request.method=='POST':
        content=request.form['name']
        content2=request.form['post']
        newTitle=Blog(name=content,post=content2)
        #newPost=Blog(post=content2)
        try:
            db.session.add(newTitle)
            #db.session.add(newPost)
            db.session.commit()
            return redirect('/blog')
        except:
            return redirect('/error')
    else:
        posts=Blog.query.all()
        return render_template('blog.html', posts=posts, form=form, title=title)

#deletes post that user inputted
@myobj.route('/delete/<int:id>')
def deletePost(id):
    delete_post = Blog.query.get_or_404(id)
    try:
        db.session.delete(delete_post)
        db.session.commit()
        return redirect ('/blog')
    except:
        return redirect('/error')




#Rendering the PROCESS of making flash card
@login_required
@myobj.route('/makeflashcards/<int:num>', methods = ['GET', 'POST'])
def makeflashcards(num):
    form = FlashCardForm()
    
    if form.validate_on_submit():  #if the user creates a new flashcard
        flashcard = Flashcard(owner = current_user.username, fctitle = form.fctitle.data, fcterm = form.fcword.data, fcdesc = form.fcdef.data, fcurl = num)
        db.session.add(flashcard)
        db.session.commit()

        displaylist.append({'term' : form.fcword.data, 'definition' : form.fcdef.data})
    
    return render_template('fccreate.html', form = form, displaylist = displaylist)


#rendering the flash card by getting the url, then by publishing it with different templates 
@login_required
@myobj.route('/renderfc/<int:num>', methods = ['GET', 'POST'])
def renderfc(num):
    currentowner =  (Flashcard.query.filter_by(fcurl = num).first()).owner == current_user.username
    form = ShareForm()
    color = 'danger'

    templist = []
    flashcards = Flashcard.query.filter_by(fcurl = num).all()
    for flashcard in flashcards:
        title = flashcard.fctitle
        templist.append({'term': flashcard.fcterm, 'description':flashcard.fcdesc})

    if form.validate_on_submit():
        if not alreadysharedwithuser(num, form.sharedwith.data.lower()):
            newShared = Sharing(owner = current_user.username,title = title, cardnumber = num, sharedwith = form.sharedwith.data.lower())
            db.session.add(newShared)
            db.session.commit()
            color = "success"
            flash(f'Shared with user {form.sharedwith.data}')
        else:
            color = "danger"
            flash(f'Error! Already shared with {form.sharedwith.data}')
            return redirect(f'/renderfc/{num}')
    

    

    
    return render_template('renderfc.html', title = title, templist = templist, form = form, color = color, currentowner = currentowner)


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

#returns urls of user's own flashcard
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

#returns true/false based on wether a flashcard is already shared with user
def alreadysharedwithuser(number, username):
    if(Sharing.query.filter_by(sharedwith = username).first() == None):
        return False 
    sharedusers = Sharing.query.filter_by(sharedwith = username.lower()).all()
    for users in sharedusers:
        if(users.cardnumber == number):
            return True
    return False

def sharedFlashCardslist():
    templist = []
    flashcards = Sharing.query.filter_by(sharedwith = current_user.username.lower()).all()
    for flashcard in flashcards:
        templist.append({'url': flashcard.cardnumber, 'title':flashcard.title, 'owner':flashcard.owner}) 
    
    return templist

def totalminutes(logintime, logouttime):
    return round((logouttime - logintime).total_seconds()/60)



@myobj.route('/admin')
def admin():
    users = User(username = 'alex', email = 'alex@gmail.com', password = generate_password_hash('password', method = 'sha256'))
    db.session.add(users)
    db.session.commit()

    flashcard = Flashcard(owner = 'alex', fctitle = 'Math', fcterm = 'Addition', fcdesc = 'To add up stuff', fcurl = 4323)
    db.session.add(flashcard)
    db.session.commit()
    flashcard = Flashcard(owner = 'alex', fctitle = 'Math', fcterm = 'Subtraction', fcdesc = 'To sum up stuff', fcurl = 4323)
    db.session.add(flashcard)
    db.session.commit()

    flashcard = Flashcard(owner = 'alex', fctitle = 'Science', fcterm = 'Rocks', fcdesc = 'Hard Stuff on Planet', fcurl = 5643)
    db.session.add(flashcard)
    db.session.commit()
    flashcard = Flashcard(owner = 'alex', fctitle = 'Science', fcterm = 'Another Rock', fcdesc = 'Another Hard stuff on planet', fcurl = 5643)
    db.session.add(flashcard)
    db.session.commit()

    flashcard = Flashcard(owner = 'alex', fctitle = 'Computer Science', fcterm = 'Java', fcdesc = 'Hard Stuff on Computer', fcurl = 4567)
    db.session.add(flashcard)
    db.session.commit()
    flashcard = Flashcard(owner = 'alex', fctitle = 'Computer Science', fcterm = 'Python', fcdesc = 'Another Hard stuff on Computer', fcurl = 4567)
    db.session.add(flashcard)
    db.session.commit()

    sharing = Sharing(owner = 'alex', title = 'Science', cardnumber = 5643, sharedwith = 'kiara')
    db.session.add(sharing)
    db.session.commit()

    tracker = Tracker(username = 'alex',logintime = 1, logouttime =1, minutes = 10)
    db.session.add(tracker)
    db.session.commit()

    tracker = Tracker(username = 'alex',logintime = 1, logouttime =1, minutes = 30)
    db.session.add(tracker)
    db.session.commit()

    tracker = Tracker(username = 'alex',logintime = 1, logouttime =1, minutes = 40)
    db.session.add(tracker)
    db.session.commit()

    tracker = Tracker(username = 'alex',logintime = 1, logouttime =1, minutes = 40)
    db.session.add(tracker)
    db.session.commit()






    users = User(username = 'kiara', email = 'kiara@gmail.com', password = generate_password_hash('password', method = 'sha256'))
    db.session.add(users)
    db.session.commit()

    flashcard = Flashcard(owner = 'kiara', fctitle = 'Art History', fcterm = 'Rome', fcdesc = 'They had stuff going on', fcurl = 6789)
    db.session.add(flashcard)
    db.session.commit()
    flashcard = Flashcard(owner = 'kiara', fctitle = 'Art History', fcterm = 'Greece', fcdesc = 'They had stuff going on too', fcurl = 6789)
    db.session.add(flashcard)
    db.session.commit()

    flashcard = Flashcard(owner = 'kiara', fctitle = 'Technology', fcterm = 'Phone', fcdesc = 'Play games on', fcurl = 6790)
    db.session.add(flashcard)
    db.session.commit()
    flashcard = Flashcard(owner = 'kiara', fctitle = 'Technology', fcterm = 'Computer', fcdesc = 'Another way to play games on', fcurl = 6790)
    db.session.add(flashcard)
    db.session.commit()

    flashcard = Flashcard(owner = 'kiara', fctitle = 'Random Stuff', fcterm = 'Paper', fcdesc = 'To Write on', fcurl = 6791)
    db.session.add(flashcard)
    db.session.commit()
    flashcard = Flashcard(owner = 'kiara', fctitle = 'Random Stuff', fcterm = 'Pencil', fcdesc = 'To write with', fcurl = 6791)
    db.session.add(flashcard)
    db.session.commit()

    sharing = Sharing(owner = 'kiara', title = 'Random Stuff', cardnumber = 6791, sharedwith = 'alex')
    db.session.add(sharing)
    db.session.commit()

    sharing = Sharing(owner = 'kiara', title = 'Technology', cardnumber = 6790, sharedwith = 'alex')
    db.session.add(sharing)
    db.session.commit()

    tracker = Tracker(username = 'kiara', logintime = 1, logouttime =1, minutes = 10)
    db.session.add(tracker)
    db.session.commit()

    tracker = Tracker(username = 'kiara',logintime = 1, logouttime =1, minutes = 26)
    db.session.add(tracker)
    db.session.commit()

    tracker = Tracker(username = 'kiara',logintime = 1, logouttime =1, minutes = 13)
    db.session.add(tracker)
    db.session.commit()

    tracker = Tracker(username = 'kiara',logintime = 1, logouttime =1, minutes = 26)
    db.session.add(tracker)
    db.session.commit()



@myobj.route('/upload')
@login_required
def upload_file():
   return render_template('upload.html')
	
@myobj.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename('test.md'))
      return redirect ('/rendernotes')

@myobj.route('/rendernotes')
def render_notes():
    readme_file = open('test.md', "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string

