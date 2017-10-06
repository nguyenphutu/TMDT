from app import db
from .base import Base

class Category(Base):
    __tablename__ = 'categorys'
    name = db.Column(db.String(255),  nullable=False, unique=True)
    url = db.Column(db.String(255),  nullable=False)

    def __repr__(self):
        return f'Category {self.name}'