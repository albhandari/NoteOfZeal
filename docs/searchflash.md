# Search Flashcards


Routes for searching
```python
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
```



### HTML

```
{% extends 'base.html' %}
{% block content %}

<br/>
<h2>You Searched For...</h2>
<p>{{ searched }}</p>


<form method = "POST" novalidate>
    {{ form.hidden_tag() }}
    <div class="card">
        <div class="card-header">
          Recent Flash-Cards
        </div>
    <div class="row">
        {% for items in templist %}
        <div class="col-sm-2">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ items.title }}</h5>
                <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                <a href="/renderfc/{{ items.url }}" class="btn btn-primary">View</a>
              </div>
            </div>
          </div>
        {% endfor %}
    </div>
</form>




{% endblock %}

<form method ="POST" action="{{ url_for('search')}}" class="d-flex">
          {{ form.hidden_tag() }}
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search", name = "searched">
          <button class="btn btn-dark" type="submit">Search</button>
          <a href="/logout" class="btn btn-danger" role="button" aria-disabled="true">Logout</a>
        </form>
```
