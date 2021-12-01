# Delete Account


Create route to delete account
```python
@myobj.route("/deleteacc")
@login_required
def deleteacc():

    currentUser = User.query.filter_by(id=current_user.id).first()
    logout_user()
    db.session.delete(currentUser)
    db.session.commit()
    flash(f'User has been deleted')

    return redirect(url_for('login'))
```



### HTML pages

```
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              DELETE ACCOUNT
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="/deleteacc">DELETE ACCOUNT!</a></li>
            </ul>
          </li>
```
