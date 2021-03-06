from app import db
from app.model.base import Base

class Category(Base):
    __tablename__ = 'categories'
    name = db.Column(db.String(255),  nullable=False, unique=True)
    url = db.Column(db.String(255),  nullable=False)

    def __repr__(self):
        return self.name