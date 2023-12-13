from flask import request, render_template, flash

from finalproject import app
from .models import Book
from .database_manager import DatabaseManager

book = Book()
print(book)


@app.route("/")
def home():
    return render_template("home.html")


#POST METHOD FORM

@app.route("/add-book", methods = ['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        if len(request.form['title'].strip()) == 0:
            print("flashing")
            flash("nope")
            return render_template("add-book.html")

        DatabaseManager.create_book(
            title = request.form['title'],
            author = request.form['author'],
            fictionality = request.form['fiction-or-not'],
            library =  request.form['to-read-or-read'] 
        )

        return f"""
            {request.form}
            Book created!
            Title: {request.form['title']} <br>
            Author: {request.form['author']} <br>
            Fiction or Not: {request.form['fiction-or-not']} <br>
            To Read or Read: {request.form['to-read-or-read']} 
        """

    return render_template("add-book.html")
