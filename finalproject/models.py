from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from . import db 


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    connections: Mapped[List["UserBookConnection"]] = relationship()

    def __repr__(self):
        return f"User({self.id}, {self.display_name}, {self.username}, {self.email}, {self.hashed_password})"

class OLBook(db.Model):
    __tablename__ = "olbooks"
    olid: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String)
    cover_id: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"OLBook({self.olid}, {self.title}, {self.author}, {self.cover_id})"

class UserBookConnection(db.Model):
    __tablename__ = "user_book_connections"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    book_olid: Mapped[str] = mapped_column(ForeignKey("olbooks.olid"), primary_key=True)
    note: Mapped[str] = mapped_column(String(100000), nullable=True)
    library: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)

    olbook: Mapped["OLBook"] = relationship()

    def __repr__(self):
        if self.note:
            note = self.note[0:50]
        else:
            note = None
        return f"UserBookConnection({self.user_id}, {self.book_olid}, {note}, {self.library})"


