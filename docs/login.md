# Login/Sign up/Sign out

Import forms

```python
from  website  import  myobj, db
from  website.forms  import  LoginForm, SignupForm, ToDoListForm, FlashCardForm,
from  website.models  import  User, ToDoList, Flashcard
```

Register, login and sign in in routes.py

```python
@myobj.route("/")
@login_required
def mainMenu():
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

        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form = form)

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

        return '<h1>New user has been created</h1>'

    return render_template('signup.html', form = form)
```

### Forms

```python
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min = 3, max = 15)])
    password = PasswordField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])
    submit = SubmitField('Sign in')

class SignupForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(),Email(message = 'Invalid email'), Length(max = 50)])
    username = StringField('Username', validators = [InputRequired(), Length(min = 3, max = 15)])
    password = PasswordField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])
    submit = SubmitField('Sign Up')
```

### HTML pages

````
{% extends 'base.html' %}

{% block content %}
{% with messages = get_flashed_messages() %}
{% if messages %}
<ul>
    {%for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
{% endwith %}


<div class="bg-body rounded mx-auto" style="width: 160px;">
    <h1>Sign Up</h1>
</div>


<div class="shadow p-3 mb-5 bg-primary bg-opacity-50 rounded mx-auto" style="width: 400px;">
    <form method = "POST" novalidate>
        {{ form.hidden_tag() }}
    
        <p>
            {{ form.email.label(class="form-label") }}
            {{ form.email(class="form-control") }}
        </p>
        <p>
            {{ form.username.label(class="form-label") }}
            {{ form.username(class="form-control") }}
        </p>
        <p>
            {{ form.password.label(class="form-label") }}
            {{ form.password(class="form-control") }}
        </p>
        <p>
            {{ form.submit(class="btn btn-primary") }}
        </p>
        
    
    </form>

</div>

{% endblock %}

{% extends 'base.html' %}

{% block content %}
{% with messages = get_flashed_messages() %}
{% if messages %}
<ul>
    {%for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
{% endwith %}


<div class="bg-body rounded mx-auto" style="width: 125px;">
    <h1>Sign in</h1>
</div>


<div class="shadow p-3 mb-5 bg-primary bg-opacity-50 rounded mx-auto" style="width: 400px;">
    <form method = "POST" novalidate>
        {{ form.hidden_tag() }}
    
        <p>
            {{ form.username.label(class="form-label") }}
            {{ form.username(class="form-control") }}
        </p>
        <p>
            {{ form.password.label(class="form-label") }}
            {{ form.password(class="form-control") }}
        </p>
        <p>
            {{ form.submit(class="btn btn-primary") }}
        </p>
        
    
    </form>

</div>


{% endblock %}
````
