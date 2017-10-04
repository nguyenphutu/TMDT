from flask import Flask, render_template, Blueprint
from app.model.user import User
from app import db
from app.service.user import UserService


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register')
def register():
    u_service = UserService(db)
    user = u_service.create_user(name='nguyen', email='sadsads@gmail.com', password='123456', role='1', status='2')
    # try:
    #     db.session.add(user)
    #     db.session.commit()
    # except Exception as e:
    #     print('Email is already exists')
    #     db.session.rollback()
    print(user)
    users = u_service.all()
    print(users)
    print(u_service.find_by_email(email='sadsads@gmail.com'))

    return render_template("login.html")

@auth.route('/login')
def login():
    return render_template("login.html")
