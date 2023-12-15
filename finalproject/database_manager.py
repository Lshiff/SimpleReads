from . import db, app
from .models import Book

from typing import Optional

# from config import app
# db.init_app(app)

with app.app_context():
    db.create_all()

class DatabaseManager:

    @staticmethod
    def create_book(title: str, author: str, rating: Optional[int] = None, fictionality: Optional[str] = None, library: Optional[str] = None):
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
    def get_all_books():
        return db.session.execute(db.select(Book)).scalars()


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



