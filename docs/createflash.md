# Create Flashcards

Route to create new flashcard
```python
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


```
Flashcard form
```python
class FlashCardForm(FlaskForm):
    fctitle = StringField('Title', validators = [InputRequired()])
    fcword = StringField('Term', validators = [InputRequired()])
    fcdef = StringField('Description', validators = [InputRequired()])
    addfc = SubmitField('Add')
```
HTML
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


<div class="bg-body rounded mx-auto" style="width: 409px;">
    <h1>Create your flashcards!</h1>
</div>


<div class="shadow p-3 mb-5 bg-primary bg-opacity-50 rounded mx-auto" style="width: 400px;">
    <form method = "POST" novalidate>
        {{ form.hidden_tag() }}
    
        <p>
            {{ form.fctitle.label(class="form-label") }}
            {{ form.fctitle(class="form-control") }}
        </p>
        <p>
            {{ form.fcword.label(class="form-label") }}
            {{ form.fcword(class="form-control") }}
        </p>
        <p>
            {{ form.fcdef.label(class="form-label") }}
            {{ form.fcdef(class="form-control") }}
        </p>
        <p>
            {{ form.addfc(class="btn btn-primary") }}
        </p>


    </form>

</div>

<div class="bg-body rounded mx-auto" style="width: 200px;">
    <a class="btn btn-dark" href="/home" role="button">Finish Creating Flashcard</a>
</div>

<br/>



<div class="row">
    {% for flashcard in displaylist %}
    <div class="col-sm-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ flashcard.term }}</h5>
                <p class="card-text">{{ flashcard.definition }}</p>
                <p class="btn btn-primary">Added </p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>





{% endblock %}
````
