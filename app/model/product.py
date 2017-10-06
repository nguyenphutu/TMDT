from .base import Base
from app import db

class Product(Base):
    __tablename__ = 'products'

    name = db.Column(db.String(255),  nullable=False)
    info = db.Column(db.Text,  nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    gia_ban = db.Column(db.Float, nullable=False)
    sale = db.Column(db.Integer, nullable=True)
    slug = db.Column(db.Text,  nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'), nullable=False)
    category = db.relationship('Category', backref='products', lazy=True)

    def __repr__(self):
        return '<Product %r>' % (self.name)