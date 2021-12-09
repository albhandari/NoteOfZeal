import datetime
from website import myobj, db
from website.models import User, ToDoList, Flashcard, Sharing, Tracker, Blog, Journal
from flask import render_template, flash, redirect, url_for, request, session
from website.forms import LoginForm, SignupForm, ToDoListForm, FlashCardForm, SearchForm, ShareForm, BlogForm, JournalForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from random import randint
from flaskext.markdown import Markdown
from werkzeug.utils import secure_filename
import markdown.extensions.fenced_code


# main variable to track login and logout time
login_utc = datetime.datetime.utcnow()
logout_utc = datetime.datetime.utcnow()




#initial Splash page
#when clicked redirected to /login
@myobj.route("/")
def mainMenu():
    return render_template('index.html')





#home page 
@myobj.route("/home")
@login_required
def home():

    #related to /makeflashcards
    #list of flashcards that are stored for rendering, and when user is redirected to /home
    #this list clears so there is a clear list for new flashcards
    displaylist.clear() 


    owner = current_user.username #Username needed for greeting

    thelist = listofurls() #list of user's flashcards' urls and titles --> Easy for rendering

    #history has user's last three sessions with progress data
    history = lastthreesessions(listofsessions(owner)) 

    return render_template('home.html', thelist = thelist, owner = owner, history = history)





#error page if there is an error
@myobj.route("/error")
@login_required
def error():


    return render_template('error.html')





#page for all the flashcards related implementation: Viewing user's own and shared flashcard and Creating Flashcard
@myobj.route("/flashboard")
@login_required
def flashboard():

    #clears list of previously created flaskcard terms to make sure there is no trouble rendering
    displaylist.clear() 

    #list of unique urls for flaskcard that hasn't been used previously
    flashcardurl = uniqueurl()

    #redirect variable for render_template to make new flashcards
    url = f'/makeflashcards/{flashcardurl}' 


    thelist = listofurls() #list of user's own flash cards for rendering
    sharedlist = sharedFlashCardslist() # list of flashcards shared with user for rendering


    return render_template('flashboard.html', url = url, thelist = thelist, sharedlist = sharedlist)





#uses current_User from flask_login to get current User id and removes from the sqldatabase
@myobj.route("/deleteacc")
@login_required
def deleteacc():

    message = deleteverything(current_user.username)
    currentUser = User.query.filter_by(id=current_user.id).first()
    logout_user()
    db.session.delete(currentUser)
    db.session.commit()
    flash(f'{message}')

    return redirect(url_for('login'))





#simple login implementation, even hashes the password in the database
@myobj.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first() #gets username from database for login credentials
        if user:
            if check_password_hash(user.password, form.password.data):  #if user exists and password matches, store login time, and redirect to home
                login_user(user, remember = False)
                login_utc = datetime.datetime.utcnow()
                return redirect(url_for('home'))

        flash(f'Invalid username or password') #if credentials don't match, returns error
    return render_template('login.html', form = form)





#wrapper to tell where to locate the form in NAV bar 
@myobj.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


#When clicked on the search on nav bar, redirects to /search to find the flashcard related to user's search term
#uses base() above to locate it as a form
@myobj.route('/search', methods = ['GET',"POST"])
def search():
    form = SearchForm()
    flashcards = Flashcard.query
    if form.validate_on_submit():
        form.searched = form.searched.data
        templist = similarity(form.searched) #templist contains all flashcard that contains what user searched, which is used for rendering
        
        return render_template('search.html', form = form, searched = form.searched, templist = templist)
    
    flash('Error: Invalid Search') #if an error happens, flashes error and redirects to home page
    return redirect('home')





#Logs user out
@myobj.route('/logout')
@login_required
def logout():

    #when user logs out, gathers the time and differences the login with logout time to store for session recording
    #Session time is then stored in the "Tracker" database
    logout_utc = datetime.datetime.utcnow() 
    sessionmins = Tracker(username = current_user.username, logintime = login_utc, logouttime = logout_utc, minutes = totalminutes(login_utc, logout_utc))
    db.session.add(sessionmins)
    db.session.commit()


    logout_user() #logs out user
    flash(f'You have successfully logged-out!')
    return redirect(url_for('login'))





#basic signup and uses hashpassword to store data too
@myobj.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    

    if form.validate_on_submit():     #if criterias for the user input meets
        hashedpassword = generate_password_hash(form.password.data, method = 'sha256')     #creates a hashed password for safety
        newUser = User(username = form.username.data, email = form.email.data, password = hashedpassword)     #creates a new user and stores in database
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
    title = "To do list"   #title for display in the html template

    #if user posts with valid inputs, then stores in 'ToDoList' database 
    #otherwise redirects to /error without saving information
    if request.method == 'POST':
        content = request.form['name']
        newtask = ToDoList(username = current_user.username, name = content)
        try:
            db.session.add(newtask)
            db.session.commit()
            return redirect('/todolist')
        except:
            return redirect('/error')
    else:
        tasks = ToDoList.query.filter_by(username = current_user.username).all() #list of tasks for rendering later
        return render_template('todolist.html', tasks = tasks, form = form, title = title)





#deletes task that user checked off from /todolist above
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





#blogpost for everyone to make posts
@myobj.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    form=BlogForm()
    title="Blog posts"
    if request.method=='POST':
        content=request.form['name']
        content2=request.form['post']
        newTitle=Blog(username = current_user.username ,title=content,post=content2)
        try:
            db.session.add(newTitle)
            db.session.commit()
            return redirect('/blog')
        except:
            return redirect('/error')
    else:
        posts=Blog.query.all()
        return render_template('blog.html', posts=posts, form=form, title=title)


#deletes post that user inputted
@login_required
@myobj.route('/del/<int:id>')
def delpost(id):
    delete_post = Blog.query.filter_by(id = id).first()
    if(delete_post != None):
        db.session.delete(delete_post)
        db.session.commit()
        return redirect ('/blog')
    else:
        redirect('/error')
    
    return redirect('/blog')



#url where flashcard can be made
@login_required
@myobj.route('/makeflashcards/<int:num>', methods = ['GET', 'POST'])
def makeflashcards(num):
    form = FlashCardForm()
    
    if form.validate_on_submit():  #if the user creates a new flashcard 

        #new term gets stored in the 'Flashcard' database
        flashcard = Flashcard(owner = current_user.username, fctitle = form.fctitle.data, fcterm = form.fcword.data, fcdesc = form.fcdef.data, fcurl = num)
        db.session.add(flashcard)
        db.session.commit()
        
        #after it's stored, the new term are also stored in a list called 'displaylist' to render them right after they are stored in database
        displaylist.append({'term' : form.fcword.data, 'definition' : form.fcdef.data})
    
    return render_template('fccreate.html', form = form, displaylist = displaylist)





#rendering the flash card by getting the url, then by publishing it with different templates 
@login_required
@myobj.route('/renderfc/<int:num>', methods = ['GET', 'POST'])
def renderfc(num):

    #currentowner is a boolean which stores True or False based on wether the current user viewing the current flashcard is the owner
    #if it's not the owner of the flashcard, then user doesn't have the ability to share
    currentowner =  (Flashcard.query.filter_by(fcurl = num).first()).owner == current_user.username
    form = ShareForm()
    color = 'danger'
    

    templist = []
    flashcards = Flashcard.query.filter_by(fcurl = num).all() #gets all the terms of the flashcard given specified url

    #stores the terms in a render-able format in templist 
    for flashcard in flashcards:
        title = flashcard.fctitle
        templist.append({'term': flashcard.fcterm, 'description':flashcard.fcdesc})
        

    if form.validate_on_submit():

        #if flashcard isn't shared specified person, then links the flashcard with the specified person and stores in the "Sharing" database
        if not alreadysharedwithuser(num, form.sharedwith.data.lower()): 
            newShared = Sharing(owner = current_user.username,title = title, cardnumber = num, sharedwith = form.sharedwith.data.lower())
            db.session.add(newShared)
            db.session.commit()
            color = "success"
            flash(f'Shared with user {form.sharedwith.data}')

        #otherwise if it is already shared, returns an error and redirects back to the flashcard url   
        else:
            color = "danger" 
            flash(f'Error! Already shared with {form.sharedwith.data}')
            return redirect(f'/renderfc/{num}')
    

    
    return render_template('renderfc.html', title = title, templist = templist, form = form, color = color, currentowner = currentowner)





#url to make journal at /makejournal
@login_required
@myobj.route('/makejournal', methods = ['GET', 'POST'])
def makejournal():
    form = JournalForm()

    if form.validate_on_submit():
        if form.jtitle.data == None or form.jdesc.data == None:
            flash('Error: Make sure you enter valid Journal entry or Title')
        else:
            newentry = Journal(owner = current_user.username, jtitle = form.jtitle.data,  jdesc = form.jdesc.data, jdate = f'{datetime.datetime.utcnow()}'[0:10])
            db.session.add(newentry)
            db.session.commit()
            flash('Success: Your journal Entry has been added')

    return render_template('makejournal.html', form = form)





#url to see all of user's journals at /renderjournal
@login_required
@myobj.route('/renderjournal', methods = ['GET', 'POST'])
def renderjournal():
    
    #all of user's journal entry is stored as a formatted list for easy endering
    alljournal = journalentrylist(current_user.username)
    
    #if user has no journal or if list that contains user's journals are empty, flashes that it is empty
    if len(alljournal) == 0:
        flash('Make journal Entries to show them here!')

    return render_template('renderjournal.html', alljournal = alljournal)
 




#/upload has a rendertemplate which has a form to upload file
#once uploaded and submitted, it is then redirected to /uploader
@myobj.route('/upload')
@login_required
def upload_file():
   return render_template('upload.html')


#/uploader basically takes in the file and saved it. Then user is redirected to /rendernotes where 
#they can see the uploaded MD file
@myobj.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename('test.md'))
      return redirect ('/rendernotes')

#using md library, this url renders the saved note
@myobj.route('/rendernotes')
def render_notes():
    readme_file = open('test.md', "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    return md_template_string








#combination of numbers from 0-9 with 4 placeholders, (first part of generating a distinct url)
def fourdigitcombo():
    return (1000 * randint(0,9)) + (100 *randint(0,9)) +  (10 * randint(0,9)) + randint(0,9)


#takes output from fourdigitcombo() and checks returns True or False based on wether the url is already used
def inthedatabase(num):
    return  db.session.query(db.exists().where(Flashcard.fcurl == num)).scalar()


#utilizes fourdigitcombo() and inthedatabase() function to return a unique url for the flashcards 
def uniqueurl():
    finalnum = fourdigitcombo()
    while(inthedatabase(finalnum)):
        finalnum = fourdigitcombo()
    return finalnum



#returns urls of user's own flashcard
#since some of the terms have the same url, it doesn't duplicate the url
def listofurls():
    #generates all the urls of flashcards
    templist = []
    flashcards = Flashcard.query.filter_by(owner = current_user.username).all()
    for flashcard in flashcards:
        templist.append({'url': flashcard.fcurl, 'title':flashcard.fctitle})
    
    #removes the duplicates and returns user's flashcard's urls
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
    
    #to make sure flashcards aren't duplicated 
    noduplicates = []
    for items in templist:
        if items not in noduplicates:
            noduplicates.append(items) 
    
    return noduplicates


#returns true/false based on wether a flashcard is already shared with user -->'username, based on input of flashcard url as 'number' 
def alreadysharedwithuser(number, username):
    if(Sharing.query.filter_by(sharedwith = username).first() == None): #if there are no flashcards that are shared with user
        return False 
    
    sharedusers = Sharing.query.filter_by(sharedwith = username.lower()).all() #all flashcards shared with user
    for users in sharedusers:
        if(users.cardnumber == number): #if a flashcard url matches with 'number' then returns True
            return True
    return False #otherwise returns false



def sharedFlashCardslist():
    templist = []
    flashcards = Sharing.query.filter_by(sharedwith = current_user.username.lower()).all()
    for flashcard in flashcards:
        templist.append({'url': flashcard.cardnumber, 'title':flashcard.title, 'owner':flashcard.owner}) 
    
    return templist

#converts total time user is online from logintime and logout time from seconds to minutes
def totalminutes(logintime, logouttime):
    return round((logouttime - logintime).total_seconds()/60)


#returns list of all the session that a given user was online, based on 'username' as input
def listofsessions(username):
    templist = []
    if (Tracker.query.filter_by(username = username).first() == None):
        return []
    sessions = Tracker.query.filter_by(username = username).all()
    for eachsession in sessions:
        templist.append(eachsession.minutes)
    
    return templist




#only suitable for return of listofsessions()
#returns a formatted list for last three online sessions of user including the percentage of each session given total time of three session 

# eg: lastthreesessions([10,20,40,80]) 
# returns [{'displaytime': '1 hour 20 minutes', 'percentage': 57}, {'displaytime': '40 minutes', 'percentage': 28}, {'displaytime': '20 minutes', 'percentage': 14}]
def lastthreesessions(list):
    finallist = []
    iterator = 1
    totalsum = 0


    #loop that runs until it grabs the last three session data or if the total sessions are less than 3, it grabs all the data
    while(iterator <= len(list) and iterator <= 3):
        finallist.append({"displaytime": f'{list[-iterator]} minutes' if list[-iterator] < 60 else f'{int(list[-iterator] / 60) } hours and {list[-iterator] % 60} minutes', 'percentage': list[-iterator]})
        totalsum += list[-iterator]
        iterator += 1
    
    #finds the percentage of each session by the total time of three sessions, to display appropriately in the frontend
    for items in finallist:
        items['percentage'] = int((items['percentage'] / totalsum) * 100)
    return finallist




#gets the Date in 'Month Day, Year' format
# 'str' format is always going to be '0000-00-00'

# eg: gateDate('2020-03-27') returns 'March 27, 2020'
def getDate(somestring):

    year = somestring[0:4]  

    monthList = [ 
        {"01":"January"}, {"02":"February"}, {"03":"March"},
        {"04":"April"}, {"05":"May"}, {"06":"June"},
        {"07":"July"}, {"08":"August"}, {"09":"September"},
        {"10":"October"}, {"11":"November"}, {"12":"December"},
    ]
    
    #maps month # of string with the actual month name in monthList
    month = monthList[int(somestring[5:7])-1][somestring[5:7]]
    day = somestring[8:10]

    return f'{month} {day}, {year}'



#reverses inputted list since the database returns in first created order
#getmostrecentlist(10,20,30) returns [30,20,10] 
def getmostrecentlist(inplist):
    templist = []
    iterator = 1
    if len(inplist) > 0:
        while iterator < len(inplist)+1:
            templist.append(inplist[-iterator])
            iterator = iterator + 1
    return templist


#returns a list of all the journal entries gives a username
#format of each item in list: ( {'date': #date of the journal#, 'title': #title of the journal#, 'entry': #journal description#, 'owner': #current username that is logged in# } )
def journalentrylist(username):
    templist = []
    if Journal.query.filter_by(owner = username).first() == None:
        return []
    
    tempjournalentry = Journal.query.filter_by(owner = username).all()
    for items in tempjournalentry:
        templist.append( {'date': getDate(items.jdate), 'title': items.jtitle, 'entry': items.jdesc, 'owner': current_user.username, } )
    
    return getmostrecentlist(templist)
    

#deletes user from all instances of database based on username    
def deleteverything(username):
    if ToDoList.query.filter_by(username = username).first() != None:
        for items in ToDoList.query.filter_by(username = username).all():
            db.session.delete(items)
            db.session.commit()
    
    if Blog.query.filter_by(username = username).first != None:
        for items in Blog.query.filter_by(username = username).all():
            db.session.delete(items)
            db.session.commit()
    
    if Flashcard.query.filter_by(owner = username).first != None:
        for items in Flashcard.query.filter_by(owner = username).all():
            db.session.delete(items)
            db.session.commit()
    
    if Tracker.query.filter_by(username = username).first != None:
        for items in Tracker.query.filter_by(username = username).all():
            db.session.delete(items)
            db.session.commit()
    
    if Sharing.query.filter_by(sharedwith = username).first != None:
        for items in Sharing.query.filter_by(sharedwith = username).all():
            db.session.delete(items)
            db.session.commit()
    
    if Journal.query.filter_by(owner = username).first != None:
        for items in Journal.query.filter_by(owner = username).all():
            db.session.delete(items)
            db.session.commit()
    
    #return message for displaying later
    return 'Successfully removed user from all database'




