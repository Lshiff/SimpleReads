from flask import request, render_template, flash, url_for
import requests
import json

from finalproject import app
from .models import Book
from .database_manager import DatabaseManager

book = Book()
print(book)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods = ['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        search_query = request.form['searchbox']

        print("REQUEST")
        req = requests.get('https://openlibrary.org/search.json', {'q': search_query, 'fields': 'title,author_name,first_sentence,cover_edition_key', 'sort': 'rating'})
        # req = requests.get('https://openlibrary.org/search.json', {'q': search_query})
        print(req.url)
        print(req)
        print(req.json())


        result = req.json()

        print()
        print("doc")
        print(result['docs'])

        

        books = []

        for doc in result['docs']:
            arg = {}
            print("Title", doc['title'])
            print("Author", doc.get('author_name'))
            print("cover?", doc.get('cover_edition_key'))
            arg['title'] = doc.get('title')
            arg['author'] = doc.get('author_name')
            cover = doc.get('cover_edition_key')
            if cover:
                cover_url = f"https://covers.openlibrary.org/b/olid/{cover}-M.jpg"
                arg['cover'] = cover_url
            else:
                arg['cover'] = None
            books.append(arg)


        # result = json.loads(req.json())
        # print(result)

        return render_template('search-result.html', books=books)
    return render_template("search-books.html")

@app.route("/list-books")
def list_books():
    books = DatabaseManager.get_all_books()
    return render_template("list-books.html", books=books)

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
        return render_template('list-books.html')
        return f"""
            {request.form}
            Book created!
            Title: {request.form['title']} <br>
            Author: {request.form['author']} <br>
            Fiction or Not: {request.form['fiction-or-not']} <br>
            To Read or Read: {request.form['to-read-or-read']} 
        """

    return render_template("add-book.html")
