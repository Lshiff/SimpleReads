from flask import request, render_template, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
import requests
from urllib.parse import urlparse

from finalproject import app, login_manager, bcrypt
from .database_manager import DatabaseManager
from .forms import RegisterForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
    return DatabaseManager.get_user_by_id(user_id)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():

        DatabaseManager.create_user(
            display_name = form.display_name.data,
            username = form.username.data,
            email = form.email.data,
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )
        flash("User created")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

login_manager.login_view = 'login'
@app.route("/login", methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():

        user = DatabaseManager.get_user_by_username_or_email(form.username_or_email.data)
        if not user:
            flash("No user")
            return render_template("login.html", form=form)

        valid_password = bcrypt.check_password_hash(user.hashed_password, form.password.data)
        if not valid_password:
            flash("Bad password")
            return render_template("login.html", form=form)

        login_user(user)

        #If there is next in the url, sends to next url
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('home')

        return redirect(next_page)

    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    flash("Logged out")
    logout_user()
    return redirect(url_for('home'))

@app.route("/book/<olid>")
def book_page(olid):
    if current_user.is_authenticated and DatabaseManager.ubc_exists(current_user.id, olid):
        user_note = DatabaseManager.get_note(current_user.id, olid)
    else:
        user_note = ""
    return render_template("book.html", olid=olid, user_note=user_note, dbm = DatabaseManager)

@app.route("/book/<olid>/<book_title>")
def book_page_redirect(olid, book_title):

    return redirect(url_for("book_page", olid=olid))

@app.route("/search", methods = ['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        search_query = request.form['searchbox']

        req = requests.get('https://openlibrary.org/search.json', {'q': search_query, 'fields': 'key,title,author_name,first_sentence,cover_edition_key', 'sort': 'rating'})
        result = req.json()

        books = []

        for doc in result['docs']:
            arg = {}
            arg['olid'] = doc.get('key').split("/works/")[1]
            arg['title'] = doc.get('title')
            arg['author'] = doc.get('author_name')
            cover = doc.get('cover_edition_key')
            if cover:
                cover_url = f"https://covers.openlibrary.org/b/olid/{cover}-M.jpg"
                arg['cover'] = cover_url
            else:
                arg['cover'] = None
            books.append(arg)

        return render_template('search-result.html', books=books)
    return render_template("search-result.html")

@app.route("/list-books")
@login_required
def list_books():

    connections = current_user.connections
    user_books = []
    for connection in connections:
        user_books.append({
            'olbook': connection.olbook,
            'connection': connection
        })

    return render_template("list-books.html", user_books=user_books)

#POST METHOD FORM

@app.route("/remove-olbook", methods=['POST'])
def remove_olbook():

    olid = request.json.get('olid')

    if current_user.is_anonymous:
        print("somethingis probably pretty wrong here")
        return f"/login?next=book/{olid}"

    if not DatabaseManager.user_book_connection_exists(current_user.id, olid):
        print("you do't have this book, smth wrong")
        return url_for('book_page', olid=olid)

    DatabaseManager.remove_user_book_connection(current_user.id, olid)
    # flash("Book has been removed")
    return '/list-books'



@app.route("/add-olbook", methods=['POST'])
def add_olbook():

    olid = request.json.get('olid')
    library = request.json.get('library')
    print(olid)

    if current_user.is_anonymous:
        flash("You must log in to add a book")
        return f"/login?next=book/{olid}"

    if not DatabaseManager.olbook_exists(olid):
        print("book doesn't exist yet")
        add_to_olbooks(olid)
        # return "book already exists in database"

    if DatabaseManager.user_book_connection_exists(current_user.id, olid):
        print("already exists")
        # flash("You already have that book added")
        return '/list-books'

    DatabaseManager.create_user_book_connection(current_user.id, olid, library)
    # flash("Book has been added")
    return '/list-books'

def add_to_olbooks(olid):
    response = requests.get(f'https://openlibrary.org/works/{olid}.json').json()

    title = response['title']
    cover_id = response['covers'][0]

    author_ids = response['authors']

    author_names = []
    for author_dict in author_ids:
        author_key = author_dict.get('author').get('key')
        res = requests.get(f'https://openlibrary.org{author_key}.json').json()
        author_name = res['name']
        author_names.append(author_name)
    print(author_names)

    if len(author_names) <= 1:
        authors = author_names[0] or None
    elif len(author_names) == 2:
        authors = f"{author_names[0]} and {author_names[1]}"
    else:
        authors = ""
        for i, author_name in enumerate(author_names):
            authors += author_name
            if i < len(author_names) - 1:
                authors += ", "
            if i == len(author_names) -2:
                authors += "and "

    print(title, cover_id, authors)

    DatabaseManager.create_olobook(
        olid = olid,
        title = title,
        author = authors,
        cover_id = cover_id
    )

    print(f"Book {title} has been created")


def add_to_user_books(olid):
    if DatabaseManager.user_book_connection_exists(current_user.id, olid):
        print("already exists")
    DatabaseManager.create_user_book_connection(current_user.id,olid)
    print("created")
    pass





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

@app.route("/save-notes", methods = ['POST'])
def save_notes():
    if current_user.is_anonymous:
        print("anon user")
        return("no user logged in")

    olid = request.json.get('olid')
    note = request.json.get('note')


    if not DatabaseManager.ubc_exists(current_user.id, olid):
        print("not added")
        return("Book not added")

    print("Incoming note:", note)

    DatabaseManager.save_notes(current_user.id, olid, note)

    return "got it: " + note

@app.route("/change-library", methods = ['POST'])
def change_library():
    if current_user.is_anonymous:
        print("anon user")
        return("no user logged in")

    olid = request.json.get('olid')
    library = request.json.get('library')


    if not DatabaseManager.ubc_exists(current_user.id, olid):
        print("not added")
        return("Book not added")

    print("Incoming library:", library)

    DatabaseManager.edit_library(current_user.id, olid, library)

    return "got it: " + library


@app.route("/admin")
def admin():
    if current_user.is_anonymous:
        return redirect(url_for('home'))
    if current_user.username != "Admin":
        return redirect(url_for('home'))

    users = DatabaseManager.get_all_users()
    return render_template('admin.html', users=users)




