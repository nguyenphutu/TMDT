from .base import Base
from app import db, app

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy

class Product(Base):
    __tablename__ = 'products'
    __searchable__ = ['name']

    name = db.Column(db.String(255),  nullable=False, unique=True)
    info = db.Column(db.Text,  nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sale = db.Column(db.Integer, nullable=True)
    slug = db.Column(db.Text,  nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='products', lazy=True)

    def __repr__(self):
        return '<Product %r>' % (self.name)

if enable_search:
    whooshalchemy.whoosh_index(app, Product)