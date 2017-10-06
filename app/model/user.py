from app import db
from app.model.base import Base
from sqlalchemy.types import Enum
from werkzeug.security import generate_password_hash, check_password_hash


# Define a User model
class AdminRole(object):
    USER = '0'
    MANAGER = '1'
    ADMIN = '2'

    enum = Enum(
        USER, MANAGER, ADMIN,
        name='admin_role_enum',
    )


class AdminStatus(object):
    INACTTIVE = '0'
    ACTIVE = '1'
    NEVER_LOGIN = '2'

    enum = Enum(
        INACTTIVE, ACTIVE, NEVER_LOGIN,
        name='admin_status_enum'
    )

class UserGender(object):
    Male = '0'
    Female = '1'

    enum = Enum(
        Male, Female,
        name='admin_role_enum',
    )



class User(Base):
    __tablename__ = 'user'
    # User Name
    first_name = db.Column(db.String(25),  nullable=False)
    last_name = db.Column(db.String(25),  nullable=False)
    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(50),  nullable=False)

    # Authorisation Data: role & status
    role = db.Column(AdminRole.enum, nullable=False, default=AdminRole.USER)
    status = db.Column(AdminStatus.enum, nullable=False, default=AdminStatus.NEVER_LOGIN)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % (self.email)

class User_Detail(Base):
    __tablename__ = 'user_detail'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user_detail', lazy=True)
    city = db.Column(db.Text,  nullable=False)
    district = db.Column(db.Text,  nullable=False)
    ward = db.Column(db.Text,  nullable=False)
    address = db.Column(db.Text,  nullable=False)
    phone = db.Column(db.String(20),  nullable=False)
    date_of_birth = db.Column(db.DateTime,  nullable=False)
    gender = db.Column(UserGender.enum, nullable=False)

    def __repr__(self):
        return '<User %r>' % (self.user)