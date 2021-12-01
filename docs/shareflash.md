# Share Flashcards

Each flashcard has its own unique URL that can be used to share
```python
def fourdigitcombo():
    return (1000 * randint(0,9)) + (100 *randint(0,9)) +  (10 * randint(0,9)) + randint(0,9)

def inthedatabase(num):
    return  db.session.query(db.exists().where(Flashcard.fcurl == num)).scalar()

def uniqueurl():
    finalnum = fourdigitcombo()
    while(inthedatabase(finalnum)):
        finalnum = fourdigitcombo()
    return finalnum
```


