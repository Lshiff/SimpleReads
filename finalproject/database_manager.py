from . import db, app
from .models import Book, User, OLBook, UserBookConnection

from typing import Optional

# from config import app
# db.init_app(app)

with app.app_context():
    db.create_all()

class DatabaseManager:

    @staticmethod
    def create_user_book_connection(user_id: int, book_olid):
        user_book_connection = UserBookConnection(user_id = user_id, book_olid = book_olid)
        with app.app_context():
            db.session.add(user_book_connection)
            db.session.commit()


    @staticmethod
    def create_olobook(olid: str, title: str, author: Optional[str] = None, cover_id: Optional[str] = None):
        olbook = OLBook(
            olid=olid,
            title=title,
            author=author,
            cover_id=cover_id
        )
        with app.app_context():
            db.session.add(olbook)
            db.session.commit()


    @staticmethod
    def create_book(title: str = "", author: str = "", rating: Optional[int] = None, fictionality: Optional[str] = None, library: Optional[str] = None):
        if not rating:
            book = Book(
                title=title,
                author = author,
                fictionality = fictionality,
                library = library
            )
        else:
            book = Book(
                title=title,
                author = author,
                rating = rating,
                fictionality = fictionality,
                library = library
            )
        with app.app_context():
            db.session.add(book)
            db.session.commit()
        return book

    @staticmethod
    def create_user(display_name: str, username: str, email: str, hashed_password: str):
        user = User(display_name=display_name, username=username, email=email, hashed_password=hashed_password)
        with app.app_context(): 
            db.session.add(user)
            db.session.commit()
        return user


    @staticmethod
    def get_all_books():
        return db.session.execute(db.select(Book)).scalars()

    @staticmethod
    def olbook_exists(olid):
        olbook = OLBook.query.filter_by(olid=olid).first()
        if olbook:
            return True
        return False

    @staticmethod
    def user_book_connection_exists(user_id, olid):
        ubc = UserBookConnection.query.filter_by(user_id=user_id).filter_by(book_olid=olid).first()
        if ubc:
            return True
        return False

    @staticmethod
    def get_user_by_id(id: int) -> Optional[User]:
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_username_or_email(username_or_email) -> Optional[User]:
        by_user = User.query.filter_by(username=username_or_email).first()
        if by_user:
            return by_user
        by_email = User.query.filter_by(email=username_or_email).first()
        if by_email:
            return by_email
        return None

    @staticmethod
    def username_exists(username) -> bool:
        user = User.query.filter_by(username=username).first()
        if user:
            return True
        return False

    @staticmethod
    def email_exists(email) -> bool:
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        return False



if __name__ == "__main__":
    print("maion creating book")
    DatabaseManager.create_book(
        title = "Percy Jackson",
        author = "Rick Riordan",
        rating = 10,
        fictionality = "Fiction",
        library = "Read"
        )
    print("maion created book")



