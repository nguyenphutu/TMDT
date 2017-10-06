from flask import Flask, render_template, Blueprint
from app.model.user import User
from app import db
from app.service.user import UserService
from app.service.category import CategoryService


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register')
def register():
    u_service = UserService(db)
    u_service.create_user(first_name='nguyen', last_name='tu', email='demo@gmail.com', password='123456')

    cate_service = CategoryService(db)
    cate = cate_service.create_category('amd Demo')
    print(cate.url)

    return render_template("login.html")

@auth.route('/login')
def login():
    return render_template("login.html")
