from flask import render_template, Blueprint, request, redirect, url_for, g
from app import db, login_manager
from app.service.user import UserService
from app.form import LoginForm, RegistrationForm, ForgotForm, CreateAccount
from flask_login import login_required, login_user, current_user, logout_user
from app.model.user import User
from app.service.category import CategoryService
from app.service.products import ProductService
from .scripts import admin_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/account', methods=['GET'])
@login_required
@admin_required
def list_accounts():
    u_service = UserService(db)
    accounts = u_service.all()
    return render_template("list_accounts.html", accounts=accounts)

@admin.route('/account/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_accounts():
    form = CreateAccount()
    u_service = UserService(db)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        user = u_service.create_user(first_name=first_name, last_name=last_name, email=email, password=password, role=role)
        if user:
            return redirect(url_for('admin.list_accounts'))
        else:
            error = "Email is already exists"
            return render_template("register.html", form=form, error=error)
    else:
        return render_template("register.html", form=form)

@admin.route('/account/<id>/<action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_required

def action_accounts(action):
    u_service = UserService(db)
    if id and action.lower() == 'delete':
        if request.method == 'POST':
            user = u_service.delete_user(user_id=id)
            if user:
                return redirect(url_for('admin.list_accounts'))
    return redirect(url_for('admin.list_accounts'))


@admin.route('/create_manager', methods = ['POST', 'GET'])
@login_required
@admin_required

def create_manager():
    form = RegistrationForm()
    if request.method == 'POST':
        u_service = UserService(db)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        user = u_service.create_user(first_name=first_name, last_name=last_name, email=email, password=password, role=role)
        if user:
            # db.session.add(user)
            # db.session.commit()
            return redirect(url_for('admin.list_accounts'))
        else:
            error = "Email is already exists"
            return render_template("create_manager.html", form=form, error=error)
    else:
        return render_template("create_manager.html", form=form)

@admin.route('/products ', methods=['GET'])
@login_required
@admin_required

def list_products():
    product_service = ProductService(db=db)
    products = product_service.all()
    return render_template("list_products.html", products=products)


@admin.route('/products/<category>', methods=['GET'])
@login_required
@admin_required

def list_cate_products(category):
    cate_service = CategoryService(db=db)
    products = cate_service.get_product_of_cate(category_name=category.lower())
    return render_template("list_products.html", products=products, category=category.title())

@admin.route('/products/<category_name>/<action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_required

def action_cate_products(category_name, action):
    cate_service = CategoryService(db=db)
    category = cate_service.find_cate_by_name(category_name=category_name)
    if action.lower() == 'create':
        pass
    if action.lower() == 'edit':
        pass
    if action.lower() == 'delete':
        pass
    return url_for("admin.list_cate_products", category=category_name.title())
