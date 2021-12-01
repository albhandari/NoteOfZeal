# ToDoList

ToDoListForm for creating new tasks
```python
class ToDoListForm(FlaskForm):
    name = StringField('Enter a task', validators = [InputRequired()])
    addtask = SubmitField('Add task')
```
Routes for ToDoList
```python

 - [ ] @myobj.route('/todolist', methods = ['GET', 'POST'])
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
```



### HTML

```
{% extends 'base.html' %}

{% block content %}


<div class="bg-body rounded mx-auto" style="width: 1900px;">
    <h1>To Do List</h1>
    <form method = "POST" novalidate>
      <p> {{form.name.label}} {{form.name (size=64)}} {{form.addtask (size=32)}} </p>
</div>
<br>
<br>

<table>
  <tr>
    <div class="bg-body rounded mx-auto" style="width: 1900px;">
        <h3>Task Actions</h3>
    
    </div>
  </tr>
  {% for task in tasks %}
  <tr>
    <td style= 'color:black;'>{{task.name}}</td>
    <td>
      <a href="delete/{{task.id}}" style="margin-left: 10px;">Delete</a>
  </tr>
  {% endfor %}
</table>

{% endblock %}
```
