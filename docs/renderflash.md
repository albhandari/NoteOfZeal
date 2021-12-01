# Render Flashcards

Routes for Rendering flashcards
```python
@login_required
@myobj.route('/renderfc/<int:num>')
def renderfc(num):
    templist = []
    flashcards = Flashcard.query.filter_by(fcurl = num).all()
    for flashcard in flashcards:
        title = flashcard.fctitle
        templist.append({'term': flashcard.fcterm, 'description':flashcard.fcdesc})
    



    return render_template('renderfc.html', title = title, templist = templist)

```



### HTML

```
{% extends 'base.html' %}

{% block content %}


<div class="mx-auto" style="width: 1000px;">
    <div class="card text-center">
        <div class="card-header">
          NotesOfZeal
        </div>
        <div class="card-body">
          <h5 class="card-title">{{title}}</h5>
        </div>
        <div class="card-footer text-muted">
          <br>
        </div>
    </div>
</div>

<br>

{% for items in templist %} 
<div class="mx-auto" style="width: 600px;">
    <div class="row">
        <div class="col-sm-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ items.term }}</h5>
            </div>
          </div>
        </div>
        <div class="col-sm-6">
          <div class="card">
            <div class="card-body">
              <p1 class="card-text">{{ items.description }}</p1>
            </div>
          </div>
        </div>
    </div>
</div>
<br>
{% endfor %}

{% endblock %}
```
