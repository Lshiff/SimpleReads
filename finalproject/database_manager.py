from typing import Optional
from sqlalchemy import func

from . import db, app
from .models import User, OLBook, UserBookConnection

with app.app_context():
    db.create_all()

class DatabaseManager:

    #Users

    @staticmethod
    def create_user(display_name: str, username: str, email: str, hashed_password: str):
        user = User(display_name=display_name, username=username, email=email, hashed_password=hashed_password)
        with app.app_context(): 
            db.session.add(user)
            db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(id: int) -> Optional[User]:
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_user_by_username_or_email(username_or_email) -> Optional[User]:
        lower_username_or_email = username_or_email.lower()
        by_user = User.query.filter(func.lower(User.username) == lower_username_or_email).first()
        if by_user:
            return by_user
        by_email = User.query.filter(func.lower(User.email) == lower_username_or_email).first()
        if by_email:
            return by_email
        return None

    @staticmethod
    def username_exists(username) -> bool:
        user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
        if user:
            return True
        return False

    @staticmethod
    def email_exists(email) -> bool:
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            return True
        return False


    #OLBooks

    @staticmethod
    def create_olobook(olid: str, title: str, author: Optional[str] = None, cover_id: Optional[str] = None):
        olbook = OLBook( olid=olid, title=title, author=author, cover_id=cover_id)
        with app.app_context():
            db.session.add(olbook)
            db.session.commit()

    @staticmethod
    def olbook_exists(olid):
        olbook = OLBook.query.filter_by(olid=olid).first()
        if olbook:
            return True
        return False


    #UserBookConnections

    @staticmethod
    def create_user_book_connection(user_id: int, book_olid, library):
        user_book_connection = UserBookConnection(user_id = user_id, book_olid = book_olid, library=library)
        with app.app_context():
            db.session.add(user_book_connection)
            db.session.commit()

    @staticmethod
    def user_book_connection_exists(user_id, olid):
        ubc = UserBookConnection.query.filter_by(user_id=user_id).filter_by(book_olid=olid).first()
        if ubc:
            return True
        return False
    @staticmethod
    def ubc_exists(user_id, olid):
        return DatabaseManager.user_book_connection_exists(user_id, olid)

    @staticmethod
    def get_ubc(user_id, book_olid):
        ubc = UserBookConnection.query.filter_by(user_id=user_id).filter_by(book_olid=book_olid).first()
        if not ubc:
            return None
        return ubc

    @staticmethod
    def get_note(user_id, book_olid):
        ubc = DatabaseManager.get_ubc(user_id, book_olid)
        if not ubc:
            return ""
        if not ubc.note:
            return ""
        print("got", ubc.note)
        return ubc.note

    @staticmethod
    def get_library(user_id, book_olid):
        ubc = db.session.query(UserBookConnection).filter(UserBookConnection.user_id == user_id).filter(UserBookConnection.book_olid == book_olid).first()
        if not ubc:
            print("no ubc get library")
            return None
        return ubc.library

    @staticmethod
    def get_rating(user_id, book_olid):
        ubc = db.session.query(UserBookConnection).filter(UserBookConnection.user_id == user_id).filter(UserBookConnection.book_olid == book_olid).first()
        if not ubc:
            print("no ubc get rating")
            return 0
        if not ubc.rating:
            return 0
        return ubc.rating

    @staticmethod
    def save_notes(user_id, book_olid, note_text):
        ubc = db.session.query(UserBookConnection).filter(UserBookConnection.user_id == user_id).filter(UserBookConnection.book_olid == book_olid).first()
        if not ubc:
            print(f"No UBC found for {user_id} and {book_olid}, couldnt add note {note_text[0:500]}")
            return "Bad lol"
        ubc.note = note_text
        db.session.add(ubc)
        db.session.commit()

    @staticmethod
    def edit_library(user_id, book_olid, library):
        ubc = db.session.query(UserBookConnection).filter(UserBookConnection.user_id == user_id).filter(UserBookConnection.book_olid == book_olid).first()
        if not ubc:
            print("no ubc edit library")
            return False
        ubc.library = library
        db.session.add(ubc)
        db.session.commit()

    @staticmethod
    def save_rating(user_id, book_olid, rating):
        ubc = db.session.query(UserBookConnection).filter(UserBookConnection.user_id == user_id).filter(UserBookConnection.book_olid == book_olid).first()
        if not ubc:
            print("no ubc save rating")
            return False
        ubc.rating = rating
        db.session.add(ubc)
        db.session.commit()

    @staticmethod
    def remove_user_book_connection(user_id, book_olid):
        ubc = db.session.query(UserBookConnection).filter(UserBookConnection.user_id == user_id).filter(UserBookConnection.book_olid == book_olid).first()
        if not ubc:
            print("bad ubc")
            return False
        db.session.delete(ubc)
        db.session.commit()
