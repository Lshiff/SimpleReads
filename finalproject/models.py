from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import db 



class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"User({self.id}, {self.display_name}, {self.username}, {self.email}, {self.hashed_password})"

class OLBook(db.Model):
    __tablename__ = "olbooks"
    olid: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String)
    cover_id: Mapped[str] = mapped_column(String)

class UserBookConnection(db.Model):
    __tablename__ = "user_book_connections"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_olid: Mapped[str] = mapped_column(String, primary_key=True)


class Book(db.Model):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    fictionality: Mapped[str] = mapped_column(String)
    library: Mapped[str] = mapped_column(String)

    def __init__(self, id = None, title=None, author=None, rating = None, fictionality=None, library=None):
        pass
        # self.title = title
        # self.author = author
        # self.rating = rating
        # self.fictionality = fictionality
        # self.library = library




# with app.app_context():
#     db.create_all()
