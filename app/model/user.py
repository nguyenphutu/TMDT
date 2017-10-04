# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.model.base import Base

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    first_name = db.Column(db.String(25),  nullable=False)
    last_name = db.Column(db.String(25),  nullable=False)
    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False,unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role = db.Column(db.SmallInteger, nullable=True)
    status = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return '<User %r>' % (self.name)