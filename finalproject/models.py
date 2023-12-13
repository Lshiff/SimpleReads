from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from . import db 

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    fictionality: Mapped[str] = mapped_column(String)
    library: Mapped[str] = mapped_column(String)



# with app.app_context():
#     db.create_all()
